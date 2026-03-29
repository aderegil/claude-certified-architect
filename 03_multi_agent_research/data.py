# data.py - Mock research data: articles, documents, and search results

# URL that simulates a timeout when fetched
TIMEOUT_URL = "https://restricted-journal.example.com/ai-surgical-planning-2025"

# Mock search index — each article has metadata and a short excerpt
ARTICLES = [
    {
        "title": "AI Diagnostic Systems Show 94% Accuracy in Radiology",
        "url": "https://journal-medical-ai.example.com/diagnostics-2024",
        "source": "Journal of Medical AI",
        "date": "2024-09-15",
        "excerpt": "A multi-center study of AI-assisted radiology found that diagnostic accuracy reached 94.2% across 12,000 chest X-rays, compared to 87.5% for radiologists working without AI assistance.",
        "keywords": ["ai", "healthcare", "diagnostics", "radiology", "accuracy", "imaging"],
    },
    {
        "title": "Machine Learning Accelerates Drug Discovery by 40%",
        "url": "https://nature-biotech.example.com/drug-discovery-ml-2025",
        "source": "Nature Biotechnology",
        "date": "2025-01-22",
        "excerpt": "Pharmaceutical companies using ML-based molecular screening reduced average drug candidate identification time from 4.5 years to 2.7 years, a 40% improvement.",
        "keywords": ["ai", "healthcare", "drug", "discovery", "machine", "learning", "pharmaceutical"],
    },
    {
        "title": "Remote Patient Monitoring with AI Reduces Hospital Readmissions",
        "url": "https://healthcare-it.example.com/rpm-ai-2025",
        "source": "Healthcare IT News",
        "date": "2025-03-08",
        "excerpt": "A 2,400-patient study across 8 hospitals found that AI-powered remote patient monitoring reduced 30-day readmission rates by 23%, saving an estimated $4.2M annually per hospital.",
        "keywords": ["ai", "healthcare", "remote", "monitoring", "readmission", "patient", "hospital"],
    },
    {
        "title": "AI-Powered Mental Health Screening Tools Show Promise",
        "url": "https://lancet-digital.example.com/mental-health-ai-2024",
        "source": "Lancet Digital Health",
        "date": "2024-11-30",
        "excerpt": "Natural language processing models analyzing patient intake forms detected depression indicators with 89% sensitivity, potentially reducing screening time by 60%.",
        "keywords": ["ai", "healthcare", "mental", "health", "screening", "nlp", "depression"],
    },
    {
        "title": "Ethical Concerns About AI Bias in Clinical Decision Support",
        "url": "https://jama.example.com/ai-bias-clinical-2025",
        "source": "JAMA",
        "date": "2025-02-14",
        "excerpt": "Analysis of 15 commercial clinical decision support systems revealed that 9 showed statistically significant performance disparities across racial groups.",
        "keywords": ["ai", "healthcare", "bias", "ethics", "clinical", "equity", "decision"],
    },
    {
        "title": "Comprehensive Review of AI in Surgical Planning",
        "url": TIMEOUT_URL,
        "source": "International Journal of Surgical AI (Restricted Access)",
        "date": "2025-03-01",
        "excerpt": "This comprehensive meta-analysis covers 47 studies on AI-assisted surgical planning across orthopedic, cardiac, and neurological procedures.",
        "keywords": ["ai", "healthcare", "surgical", "planning", "meta-analysis", "restricted"],
    },
]

# Full document content — keyed by URL
DOCUMENTS = {
    "https://journal-medical-ai.example.com/diagnostics-2024": {
        "title": "AI Diagnostic Systems Show 94% Accuracy in Radiology",
        "source": "Journal of Medical AI",
        "date": "2024-09-15",
        "content": (
            "Study: AI-Assisted Radiology Diagnostic Accuracy\n\n"
            "A multi-center randomized controlled trial conducted across 15 hospitals "
            "evaluated AI-assisted chest X-ray interpretation.\n\n"
            "Key Findings:\n"
            "- AI-assisted diagnosis: 94.2% accuracy (95% CI: 93.1-95.3%)\n"
            "- Radiologists without AI: 87.5% accuracy (95% CI: 86.0-89.0%)\n"
            "- AI-only (no radiologist review): 91.8% accuracy\n"
            "- Time per case: AI-assisted reduced from 4.2 minutes to 2.1 minutes\n\n"
            "The study enrolled 12,847 patients across diverse demographics. AI showed "
            "particular improvement in detecting early-stage pneumonia and subtle fractures.\n\n"
            "Limitations: The study used a specific commercial AI system (RadAssist v3.2) "
            "and results may not generalize to other AI platforms. Training data composition "
            "was not independently audited for demographic representation.\n\n"
            "Authors: Dr. Sarah Chen, Dr. Michael Torres, Dr. Aisha Patel\n"
            "Published: September 15, 2024"
        ),
    },
    "https://nature-biotech.example.com/drug-discovery-ml-2025": {
        "title": "Machine Learning Accelerates Drug Discovery by 40%",
        "source": "Nature Biotechnology",
        "date": "2025-01-22",
        "content": (
            "Machine Learning in Pharmaceutical Drug Discovery\n\n"
            "Analysis of ML-based molecular screening across 23 pharmaceutical companies "
            "from 2020-2024.\n\n"
            "Key Findings:\n"
            "- Average drug candidate identification: 2.7 years (ML-assisted) vs 4.5 years (traditional)\n"
            "- 40% reduction in time-to-candidate\n"
            "- Cost savings: estimated $150M per successful drug candidate\n"
            "- ML models identified 3 candidates that traditional screening missed\n"
            "- False positive rate: 12% for ML vs 8% for traditional (tradeoff: speed vs precision)\n\n"
            "Note: Two independent analyses disagree on cost savings. PharmaTech Analytics "
            "reports $150M savings per candidate, while the WHO Health Economics Division "
            "estimates $95M, citing different baseline assumptions and excluded costs.\n\n"
            "Methodology: Retrospective analysis comparing matched pairs of drug discovery "
            "programs (ML-assisted vs traditional) within the same company and therapeutic area.\n\n"
            "Authors: Dr. James Liu, Dr. Emma Andersson\n"
            "Published: January 22, 2025"
        ),
    },
    "https://healthcare-it.example.com/rpm-ai-2025": {
        "title": "Remote Patient Monitoring with AI Reduces Hospital Readmissions",
        "source": "Healthcare IT News",
        "date": "2025-03-08",
        "content": (
            "AI-Powered Remote Patient Monitoring: Multi-Hospital Study\n\n"
            "2,400-patient prospective study across 8 major hospital systems, 2023-2024.\n\n"
            "Key Findings:\n"
            "- 30-day readmission rate: 8.3% (AI-RPM) vs 10.8% (standard care) — 23% reduction\n"
            "- Annual cost savings: $4.2M per hospital (estimated)\n"
            "- Patient satisfaction: 4.3/5.0 (AI-RPM) vs 3.8/5.0 (standard care)\n"
            "- Alert accuracy: 91% of AI-generated alerts were clinically actionable\n"
            "- False alarm rate: 9% (down from 34% in previous-generation systems)\n\n"
            "The AI system monitored vital signs, medication adherence, and activity patterns. "
            "It used predictive models to identify patients at high risk of readmission within "
            "72 hours.\n\n"
            "Demographics: 52% female, mean age 67, 38% Medicare, 22% Medicaid. "
            "Chronic conditions: heart failure (45%), COPD (28%), diabetes (27%).\n\n"
            "Authors: Dr. Rachel Kim, Dr. David Okafor\n"
            "Published: March 8, 2025"
        ),
    },
    "https://lancet-digital.example.com/mental-health-ai-2024": {
        "title": "AI-Powered Mental Health Screening Tools Show Promise",
        "source": "Lancet Digital Health",
        "date": "2024-11-30",
        "content": (
            "NLP-Based Depression Screening: Validation Study\n\n"
            "Prospective validation of NLP models analyzing patient intake forms for "
            "depression indicators.\n\n"
            "Key Findings:\n"
            "- Sensitivity: 89% (detecting true cases)\n"
            "- Specificity: 78% (correctly identifying non-cases)\n"
            "- Screening time reduction: 60% compared to standard PHQ-9 administration\n"
            "- Model performance was consistent across age groups (18-65+)\n"
            "- Performance gap: sensitivity dropped to 71% for non-English intake forms\n\n"
            "The model was trained on 50,000 de-identified intake forms with confirmed "
            "PHQ-9 scores. It analyzed free-text responses, noting linguistic markers "
            "associated with depression.\n\n"
            "Ethical Note: The authors emphasize this tool is for screening support, not "
            "diagnosis. All positive screens require clinician confirmation. The 22% false "
            "positive rate means approximately 1 in 5 flagged patients may not meet "
            "diagnostic criteria.\n\n"
            "Authors: Dr. Lisa Nakamura, Dr. Ahmed Hassan\n"
            "Published: November 30, 2024"
        ),
    },
    "https://jama.example.com/ai-bias-clinical-2025": {
        "title": "Ethical Concerns About AI Bias in Clinical Decision Support",
        "source": "JAMA",
        "date": "2025-02-14",
        "content": (
            "AI Bias in Clinical Decision Support: Systematic Review\n\n"
            "Systematic analysis of 15 commercial clinical decision support (CDS) systems "
            "deployed in US hospitals.\n\n"
            "Key Findings:\n"
            "- 9 of 15 systems (60%) showed statistically significant performance disparities "
            "across racial groups\n"
            "- Largest disparity: one dermatology AI showed 31% lower accuracy for darker "
            "skin tones\n"
            "- 4 systems showed >10% accuracy gap between highest and lowest performing "
            "demographic groups\n"
            "- Only 3 of 15 vendors provided demographic performance breakdowns\n"
            "- Hospitals using biased systems were 2.3x more likely to have inequitable "
            "treatment outcomes\n\n"
            "Recommendations:\n"
            "1. Mandate demographic performance reporting for all clinical AI systems\n"
            "2. Require pre-deployment equity audits with independent validation\n"
            "3. Establish minimum performance thresholds across all demographic groups\n"
            "4. Create ongoing monitoring systems for deployed AI tools\n\n"
            "Authors: Dr. Maria Rodriguez, Dr. Kevin Washington, Dr. Priya Sharma\n"
            "Published: February 14, 2025"
        ),
    },
}
