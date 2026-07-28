from chains.summarize_chain import summarize
from chains.classify_chain import classify
from word_count import count_words

from chains.summarize_chain import summarize
from chains.classify_chain import classify
from word_count import count_words
 
SAMPLE_INPUTS = [
    (
        "business_sample",
        "Our quarterly earnings report shows a 12% increase in revenue, driven "
        "primarily by strong performance in the enterprise software division. "
        "The board has approved a new budget for expanding the sales team into "
        "European markets next fiscal year, with a focus on partnerships with "
        "regional distributors.",
    ),
    (
        "health_sample",
        "Regular exercise combined with a balanced diet has been shown to "
        "significantly reduce the risk of cardiovascular disease. Doctors "
        "recommend at least 150 minutes of moderate aerobic activity per week, "
        "along with adequate sleep and stress management, to maintain long-term "
        "heart health.",
    ),
    (
        "business_sample_long",
        "Our quarterly earnings report shows a 12% increase in revenue, driven "
        "primarily by strong performance in the enterprise software division, "
        "which grew 28% year-over-year and now accounts for nearly half of total "
        "company revenue. The consumer hardware division, by contrast, saw a "
        "modest 3% decline, which management attributes to ongoing supply chain "
        "disruptions in Southeast Asia and increased competition from lower-cost "
        "manufacturers. The board has approved a new budget for expanding the "
        "sales team into European markets next fiscal year, with a focus on "
        "partnerships with regional distributors in Germany, France, and the "
        "Netherlands. This expansion is expected to cost approximately 8 million "
        "dollars in the first year, with break-even projected by the third "
        "quarter of the following fiscal year. Additionally, the company "
        "announced a share buyback program worth 50 million dollars, signaling "
        "confidence in long-term growth despite short-term headwinds in the "
        "hardware segment. Analysts have responded positively, with several "
        "firms raising their price targets following the announcement.",
    ),
    (
        "health_sample_long",
        "Regular exercise combined with a balanced diet has been shown to "
        "significantly reduce the risk of cardiovascular disease, according to "
        "a decade-long study following over 40,000 participants across multiple "
        "countries. Doctors recommend at least 150 minutes of moderate aerobic "
        "activity per week, such as brisk walking or cycling, along with two "
        "sessions of strength training to maintain muscle mass and bone density "
        "as people age. The study also found that sleep quality played a "
        "surprisingly large role in cardiovascular outcomes: participants who "
        "slept fewer than six hours per night had a substantially higher "
        "incidence of heart disease, even when their exercise and diet habits "
        "were otherwise similar to well-rested participants. Stress management "
        "techniques, including meditation and regular social contact, were "
        "linked to lower blood pressure and reduced inflammation markers. "
        "Researchers caution that no single factor fully explains cardiovascular "
        "risk, and that exercise, diet, sleep, and stress management appear to "
        "interact with each other rather than operating independently.",
    ),
]



def run_pipeline(label: str, text: str) -> None:
    print(f"\n=== {label} ===")
    print(f"Original ({count_words(text)} words):\n{text}\n")

    summary = summarize(text)
    print(f"Summary:\n{summary}\n")

    summary_word_count = count_words(summary)
    print(f"Summary word count: {summary_word_count}")

    topic = classify(summary)
    print(f"Classified topic: {topic}")


if __name__ == "__main__":
    for label, text in SAMPLE_INPUTS:
        run_pipeline(label, text)