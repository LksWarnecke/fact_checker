from difflib import get_close_matches
from utils.topics import TOPICS

def find_matching_topics(user_input, max_results=3):
    user_input = user_input.lower()
    candidates = []

    for topic, data in TOPICS.items():
        if user_input in topic.lower():
            candidates.append(topic)
        else:
            for kw in data["keywords"]:
                if user_input in kw.lower():
                    candidates.append(topic)
                    break

    # Fallback: fuzzy match if no exact keyword matches
    if not candidates:
        all_keywords = {topic: [topic.lower()] + data["keywords"] for topic, data in TOPICS.items()}
        flattened = [(topic, kw) for topic, kws in all_keywords.items() for kw in kws]
        matches = get_close_matches(user_input, [kw for _, kw in flattened], n=max_results, cutoff=0.5)
        for match in matches:
            for topic, kw in flattened:
                if kw == match:
                    candidates.append(topic)
                    break

    # Remove duplicates and return unique matches
    return list(dict.fromkeys(candidates))[:max_results]
