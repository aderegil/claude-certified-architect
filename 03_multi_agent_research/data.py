# data.py - Mock research data for subagent tools

# Mock web search results keyed by subtopic keyword
# Each result includes title, url, excerpt, and date for provenance tracking (task 5.6)
SEARCH_RESULTS = {
    "diagnosis": [
        {
            "title": "AI-Powered Diagnostic Imaging: A Systematic Review",
            "url": "https://example.com/ai-diagnostic-review-2024",
            "excerpt": (
                "Deep learning models achieved 94.5% accuracy in detecting early-stage "
                "lung nodules, compared to 87.2% for radiologists working without AI "
                "assistance. However, the highest accuracy (97.1%) was achieved when "
                "radiologists used AI as a second opinion tool."
            ),
            "date": "2024-03-15"
        },
        {
            "title": "FDA-Cleared AI Medical Devices: 2024 Landscape",
            "url": "https://example.com/fda-ai-devices-2024",
            "excerpt": (
                "The FDA has cleared over 950 AI-enabled medical devices as of January "
                "2024, with radiology accounting for 75% of clearances. Cardiology and "
                "ophthalmology follow at 11% and 5% respectively."
            ),
            "date": "2024-01-28"
        },
        {
            "title": "Bias in Medical AI: Dermatology Case Study",
            "url": "https://example.com/ai-bias-dermatology",
            "excerpt": (
                "Skin cancer detection models trained predominantly on lighter skin tones "
                "showed 20% lower sensitivity for melanoma detection in patients with "
                "darker skin tones, raising concerns about health equity in AI-assisted "
                "diagnosis."
            ),
            "date": "2024-06-10"
        }
    ],
    "drug_discovery": [
        {
            "title": "AI-Accelerated Drug Discovery Pipeline Results",
            "url": "https://example.com/ai-drug-discovery-2024",
            "excerpt": (
                "The first AI-designed drug (INS018_055) entered Phase II clinical trials "
                "for idiopathic pulmonary fibrosis. The compound was identified and "
                "optimized in 18 months, compared to the typical 4-5 year timeline for "
                "traditional drug discovery."
            ),
            "date": "2024-02-20"
        },
        {
            "title": "Machine Learning in Protein Structure Prediction",
            "url": "https://example.com/protein-structure-ml",
            "excerpt": (
                "AlphaFold has predicted structures for over 200 million proteins, "
                "enabling researchers to identify potential drug targets 60% faster. "
                "However, predicted structures require experimental validation before "
                "use in drug design."
            ),
            "date": "2024-04-12"
        },
        {
            "title": "Cost Analysis: AI vs Traditional Drug Development",
            "url": "https://example.com/ai-drug-cost-analysis",
            "excerpt": (
                "AI-assisted drug development reduced preclinical costs by an average "
                "of 30-40%, primarily through improved target identification and reduced "
                "late-stage failure rates. Total development timelines decreased from "
                "12-15 years to 8-10 years in early adopter programs."
            ),
            "date": "2023-11-05"
        }
    ],
    "patient_care": [
        {
            "title": "AI in Hospital Operations: Predictive Scheduling",
            "url": "https://example.com/ai-hospital-operations",
            "excerpt": (
                "Hospitals using AI-driven predictive scheduling reduced patient wait "
                "times by 35% and improved operating room utilization from 68% to 82%. "
                "Staff satisfaction scores increased 15% due to more predictable shift "
                "patterns."
            ),
            "date": "2024-05-22"
        },
        {
            "title": "Remote Patient Monitoring with AI: Outcomes Study",
            "url": "https://example.com/remote-monitoring-ai",
            "excerpt": (
                "AI-enhanced remote monitoring reduced 30-day hospital readmission rates "
                "by 28% for chronic heart failure patients. The system identified "
                "deterioration patterns an average of 3.2 days before clinical symptoms "
                "became apparent."
            ),
            "date": "2024-07-01"
        },
        {
            "title": "Clinical Decision Support Systems: Adoption Barriers",
            "url": "https://example.com/cdss-adoption-barriers",
            "excerpt": (
                "Despite demonstrated benefits, only 38% of surveyed hospitals have "
                "fully integrated AI clinical decision support. Top barriers cited: "
                "integration with existing EHR systems (67%), physician trust (54%), "
                "and regulatory uncertainty (48%)."
            ),
            "date": "2024-03-30"
        }
    ]
}


# Mock analysis findings — structured claim-source mappings (task 5.6)
# Each finding preserves provenance: claim, source_url, excerpt, date, confidence
ANALYSIS_FINDINGS = {
    "diagnosis": [
        {
            "claim": "AI diagnostic tools achieve highest accuracy when used alongside radiologists rather than replacing them",
            "source_url": "https://example.com/ai-diagnostic-review-2024",
            "excerpt": "the highest accuracy (97.1%) was achieved when radiologists used AI as a second opinion tool",
            "date": "2024-03-15",
            "confidence": "high"
        },
        {
            "claim": "Radiology dominates FDA-cleared AI medical devices at 75% of all clearances",
            "source_url": "https://example.com/fda-ai-devices-2024",
            "excerpt": "radiology accounting for 75% of clearances",
            "date": "2024-01-28",
            "confidence": "high"
        },
        {
            "claim": "AI diagnostic models show significant bias when training data lacks demographic diversity",
            "source_url": "https://example.com/ai-bias-dermatology",
            "excerpt": "20% lower sensitivity for melanoma detection in patients with darker skin tones",
            "date": "2024-06-10",
            "confidence": "high"
        }
    ],
    "drug_discovery": [
        {
            "claim": "AI can reduce drug discovery timelines from 4-5 years to 18 months for initial compound identification",
            "source_url": "https://example.com/ai-drug-discovery-2024",
            "excerpt": "identified and optimized in 18 months, compared to the typical 4-5 year timeline",
            "date": "2024-02-20",
            "confidence": "high"
        },
        {
            "claim": "AI-predicted protein structures still require experimental validation before drug design use",
            "source_url": "https://example.com/protein-structure-ml",
            "excerpt": "predicted structures require experimental validation before use in drug design",
            "date": "2024-04-12",
            "confidence": "medium"
        },
        {
            "claim": "AI-assisted development reduces preclinical costs by 30-40%",
            "source_url": "https://example.com/ai-drug-cost-analysis",
            "excerpt": "reduced preclinical costs by an average of 30-40%",
            "date": "2023-11-05",
            "confidence": "medium"
        }
    ],
    "patient_care": [
        {
            "claim": "AI predictive scheduling reduces patient wait times by 35% and improves OR utilization to 82%",
            "source_url": "https://example.com/ai-hospital-operations",
            "excerpt": "reduced patient wait times by 35% and improved operating room utilization from 68% to 82%",
            "date": "2024-05-22",
            "confidence": "high"
        },
        {
            "claim": "AI remote monitoring can predict patient deterioration 3.2 days before clinical symptoms appear",
            "source_url": "https://example.com/remote-monitoring-ai",
            "excerpt": "identified deterioration patterns an average of 3.2 days before clinical symptoms became apparent",
            "date": "2024-07-01",
            "confidence": "high"
        },
        {
            "claim": "Only 38% of hospitals have fully integrated AI clinical decision support despite proven benefits",
            "source_url": "https://example.com/cdss-adoption-barriers",
            "excerpt": "only 38% of surveyed hospitals have fully integrated AI clinical decision support",
            "date": "2024-03-30",
            "confidence": "high"
        }
    ]
}


# task 5.3 — structured error context for simulated timeout
# Includes failure_type, attempted_query, partial_results, and alternatives
# This enables intelligent coordinator recovery decisions
TIMEOUT_ERROR = {
    "failure_type": "timeout",
    "attempted_query": "AI applications in drug discovery and pharmaceutical development",
    "partial_results": [
        {
            "title": "AI-Accelerated Drug Discovery Pipeline Results",
            "url": "https://example.com/ai-drug-discovery-2024",
            "excerpt": "The first AI-designed drug entered Phase II clinical trials..."
        }
    ],
    "alternatives": [
        "Retry with a narrower query: 'AI in Phase II clinical trial optimization'",
        "Use cached results from previous searches on related topics",
        "Skip this subtopic and annotate as a coverage gap in synthesis"
    ]
}
