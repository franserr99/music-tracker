from bs4 import BeautifulSoup
import pymongo
# from urllib.request import urlopen


def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["tracker"]
    collection = db["qna"]

    with open('content.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    bs = BeautifulSoup(html_content, 'html.parser')

    content = bs.find('div', {'class': 'm-detail--body'}
                      ).find('p').find_next_siblings('p')

    for paragraph in content:
        # iterate over the children now
        question_text = ""
        answer_text = ""
        reached_answer = False

        for element in paragraph.children:

            if element.name == 'strong' and element.find('br') is not None:
                reached_answer = True
            text = str(element.get_text())
            if not reached_answer and not element.name == 'br':
                if 'Related' not in text:
                    text = text.split("Question:")[0]
                    question_text += text

            elif reached_answer:

                if 'Answer:' in text:
                    text = text.split("Answer:")[1]
                answer_text += text
        if len(question_text) > 0 and len(answer_text) > 0:
            qna = {"_id": question_text.strip(), "answer": answer_text.strip()}
            try:
                collection.insert_one(qna)
            except pymongo.errors.DuplicateKeyError:
                print(f"Duplicate question found: {question_text.strip()}")

    pass


if __name__ == "__main__":
    main()
