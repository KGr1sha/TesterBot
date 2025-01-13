from database.operations import update_test_score, add_user_statistics

def parse_questions(test: str) -> list[str]:
    questions = []
    for q in test.split("==="):
        if len(q.splitlines()) >= 1:
            questions.append(q)
    return questions


def parse_answers(question: str) -> list[str]:
    answers = []
    lines = question.splitlines()
    for line in lines:
        if not line: continue
        line = line.lstrip()
        if line[0] in "abcdABCD" and line[1] == ")":
            answers.append(line)
    return answers


async def save_score(response: str, user_id: int, test_id: int) -> bool:
    if sum([x in response for x in "[/]"]) != 3: return False

    # finding [ and ] from the end of the message
    pos1 = 0
    pos2 = 0
    sep = 0
    for i in range(len(response) - 1, -1, -1):
        if response[i] == ']':
            pos2 = i
        elif response[i] == '/':
            sep = i
        elif response[i] == '[':
            pos1 = i
            break

    right = int(response[pos1 + 1:sep])
    total = int(response[sep + 1:pos2])

    await update_test_score(test_id, f"{right}/{total}")
    user = await add_user_statistics(
        user_id,
        right,
        total
    )
    return user != None;


def get_test_time(time_str: str) -> int:
    int_str = ""
    i = 0
    while i < len(time_str) and not time_str[i].isdigit():
        i += 1
    if i == len(time_str): return -1
    while i < len(time_str) and time_str[i].isdigit():
        int_str += time_str[i]
        i += 1

    return int(int_str)
