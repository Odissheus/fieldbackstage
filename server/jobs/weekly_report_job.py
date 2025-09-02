import datetime as dt
import hashlib
from pathlib import Path
from sqlalchemy.orm import Session
from server.report_render import render_weekly_report
from server.report_pdf import html_to_pdf_bytes
from server.db import get_session, init_db
from server.models import InsightRaw, WeeklyReport


def build_context_example():
    return {
        "tenant": {"name": "PharmaX"},
        "product_line": {"name": "Cardio"},
        "week": {"id": "2025-W33"},
        "executive_summary": {"bullets": ["Obiezioni su dosaggio in crescita", "Richieste di materiali educazionali"]},
        "heatmap": {"bins": [{"territoryName": "Lombardia", "value": 27}, {"territoryName": "Lazio", "value": 14}]},
        "ci_summary": {"bullets": ["Competitor A spinge claim X", "Evento Y con relatore Z"], "thumbnails": []},
        "contributors": ["Mario Rossi", "Giulia Bianchi"],
        "kpi": {"insightsCount": 42, "positive": 10, "negative": 6, "neutral": 26},
        "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "doc_hash": "stubhash",
    }


def aggregate_week(session: Session, product_line_id: str, week_id: str) -> dict:
    # Semplice aggregazione: prendi ultimi insight della linea
    insights = (
        session.query(InsightRaw)
        .filter(InsightRaw.product_line_id == product_line_id)
        .order_by(InsightRaw.created_at.desc())
        .limit(20)
        .all()
    )
    bullets = []
    pos = neg = neu = 0
    for ins in insights:
        if ins.text:
            bullets.append(ins.text[:160])
        if ins.extracted and isinstance(ins.extracted, dict):
            s = (ins.extracted or {}).get("sentiment")
            if s == "positive":
                pos += 1
            elif s == "negative":
                neg += 1
            else:
                neu += 1
    heat_bins = {}
    for ins in insights:
        key = ins.territory_id or "n/a"
        heat_bins[key] = heat_bins.get(key, 0) + 1
    heatmap = {"bins": [{"territoryName": k, "value": v} for k, v in heat_bins.items()]}
    contributors = ["Contributore" for _ in set([ins.id for ins in insights])]  # placeholder
    return {
        "executive_summary": {"bullets": bullets[:8] or ["Nessun dato"]},
        "ci_summary": {"bullets": []},
        "heatmap": heatmap,
        "contributors": contributors,
        "kpi": {"insightsCount": len(insights), "positive": pos, "negative": neg, "neutral": neu},
    }


def run_weekly(product_line_id: str = "pl-demo", week_id: str = "2025-W33", tenant_id: str | None = None):
    init_db()
    session = next(get_session())
    agg = aggregate_week(session, product_line_id, week_id)
    ctx = {
        "tenant": {"name": "DemoTenant"},
        "product_line": {"name": product_line_id},
        "week": {"id": week_id},
        "executive_summary": agg["executive_summary"],
        "heatmap": agg["heatmap"],
        "ci_summary": agg["ci_summary"],
        "contributors": agg["contributors"],
        "kpi": agg["kpi"],
        "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "doc_hash": "",
    }
    html = render_weekly_report(ctx)
    pdf = html_to_pdf_bytes(html)
    doc_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()
    ctx["doc_hash"] = doc_hash
    out_dir = Path.cwd()
    (out_dir / "weekly_report.html").write_text(html, encoding="utf-8")
    (out_dir / "weekly_report.pdf").write_bytes(pdf)
    # CSV semplice con KPI e heatmap
    import csv
    csv_path = out_dir / "weekly_report.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["insightsCount", agg["kpi"]["insightsCount"]])
        w.writerow(["positive", agg["kpi"]["positive"]])
        w.writerow(["neutral", agg["kpi"]["neutral"]])
        w.writerow(["negative", agg["kpi"]["negative"]])
        w.writerow([])
        w.writerow(["territory", "value"])
        for b in agg["heatmap"]["bins"]:
            w.writerow([b["territoryName"], b["value"]])

    wr = WeeklyReport(
        tenant_id=tenant_id,
        product_line_id=product_line_id,
        week_id=week_id,
        executive_summary="\n".join(agg["executive_summary"]["bullets"]),
        ci_summary="\n".join(agg["ci_summary"].get("bullets", [])),
        heatmap=agg["heatmap"],
        contributors=agg["contributors"],
        url_pdf=str(out_dir / "weekly_report.pdf"),
        url_html=str(out_dir / "weekly_report.html"),
        hash=doc_hash,
    )
    session.add(wr)
    session.commit()
    
    # Index report for RAG Q&A system
    try:
        from .ai_services import index_report_for_rag
        index_report_for_rag(
            report_id=wr.id,
            executive_summary=wr.executive_summary,
            ci_summary=wr.ci_summary or "",
            week_id=wr.week_id,
            tenant_id=wr.tenant_id or "",
            product_line_id=wr.product_line_id
        )
        print(f"Report {wr.id} indexed for RAG Q&A")
    except Exception as e:
        print(f"Failed to index report for RAG: {e}")
    
    print("Report generato e salvato: ", wr.id)


if __name__ == "__main__":
    run_weekly()

