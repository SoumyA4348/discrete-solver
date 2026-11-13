"""Builds train_generated.csv: template-based paraphrases for each operation.

Run:  python combinatorics_solver/generate_data.py
The output is deterministic (fixed seed). eval_questions.csv is hand-written and never used here.
"""
import os
import random

import pandas as pd

_DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 7
PER_OPERATION = 520

WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 15: "fifteen", 20: "twenty"}

PEOPLE = ["students", "players", "employees", "candidates", "athletes", "volunteers", "musicians",
          "engineers", "members", "teachers", "contestants", "delegates", "scientists", "chefs"]
ITEMS = ["books", "toys", "paintings", "trophies", "marbles", "cards", "flags", "plants", "photos",
         "gadgets", "coins", "tickets", "stamps", "jars", "lamps", "records"]
FLAVORS = ["ice cream flavors", "pizza toppings", "sandwich fillings", "juice types", "cake varieties",
           "donut kinds", "tea blends", "soup choices", "bagel types", "cookie kinds"]
ROLES = ["a president, a secretary and a treasurer", "a captain, a vice-captain and a coach",
         "a gold, silver and bronze medalist", "a lead, a backup and a reserve", "a chair and a deputy chair"]


def num(rng, value):
    """Writes a number as a digit or, sometimes, as a word."""
    return WORDS[value] if value in WORDS and rng.random() < 0.3 else str(value)


def pair(rng, lo=2, hi=12):
    n = rng.randint(lo + 1, hi)
    return n, rng.randint(lo, n - 1)


def permutations(rng):
    n, r = pair(rng)
    p, i = rng.choice(PEOPLE), rng.choice(ITEMS)
    return rng.choice([
        f"In how many ways can {num(rng, r)} of {num(rng, n)} {p} be lined up for a photo in order?",
        f"How many ways can {num(rng, n)} {p} finish first, second and third in a race?",
        f"How many ordered arrangements of {num(rng, r)} {i} can be chosen from {num(rng, n)} different {i}?",
        f"A shelf has room for {num(rng, r)} {i}; there are {num(rng, n)} different {i} to choose from. How many arrangements are possible if order matters?",
        f"From {num(rng, n)} {p}, how many ways can we select {rng.choice(ROLES)}? Each person holds at most one position.",
        f"How many different {num(rng, r)}-letter codes can be made from {num(rng, n)} distinct letters if no letter repeats?",
        f"In how many ways can {num(rng, n)} different {i} be arranged in a row?",
        f"How many permutations of {num(rng, r)} objects can be made from a set of {num(rng, n)} distinct objects?",
        f"{num(rng, n).capitalize()} {p} enter a contest and the top {num(rng, r)} are ranked. How many possible rankings are there?",
        f"How many ways can you seat {num(rng, r)} of {num(rng, n)} {p} in {num(rng, r)} numbered chairs?",
        f"Find the number of ways to arrange {num(rng, r)} {i} out of {num(rng, n)} on a display, with no repeats and order important.",
    ])


def combinations(rng):
    n, r = pair(rng)
    p, i, f = rng.choice(PEOPLE), rng.choice(ITEMS), rng.choice(FLAVORS)
    return rng.choice([
        f"In how many ways can a committee of {num(rng, r)} be chosen from {num(rng, n)} {p}?",
        f"How many ways can you pick {num(rng, r)} {i} from a box of {num(rng, n)} different {i}, if order does not matter?",
        f"A team of {num(rng, r)} must be selected from {num(rng, n)} {p}. How many different teams are possible?",
        f"How many different hands of {num(rng, r)} cards can be dealt from {num(rng, n)} distinct cards?",
        f"Out of {num(rng, n)} {p}, {num(rng, r)} will be chosen to attend a conference. How many groups are possible?",
        f"How many subsets of size {num(rng, r)} does a set of {num(rng, n)} elements have?",
        f"A menu offers {num(rng, n)} {f}. How many ways can a customer choose {num(rng, r)} different ones?",
        f"How many ways are there to select {num(rng, r)} {p} from a group of {num(rng, n)} for a panel with no roles?",
        f"Compute the number of {num(rng, r)}-element selections from {num(rng, n)} distinct {i}, ignoring order.",
        f"A lottery draws {num(rng, r)} different numbers from {num(rng, n)}. How many possible draws are there?",
        f"How many handshakes occur if {num(rng, n)} {p} each shake hands with every other exactly once?"
        if r == 2 else f"In how many ways can {num(rng, r)} {p} be picked out of {num(rng, n)} to form a group?",
    ])


def combinations_with_replacement(rng):
    n, r = rng.randint(3, 10), rng.randint(2, 12)
    f, i = rng.choice(FLAVORS), rng.choice(ITEMS)
    return rng.choice([
        f"A shop sells {num(rng, n)} kinds of {f.split()[0]} treats. How many ways can you buy {num(rng, r)} treats if you may repeat kinds and order does not matter?",
        f"How many ways can {num(rng, r)} identical {i} be distributed among {num(rng, n)} different boxes?",
        f"How many non-negative integer solutions does x1 + x2 + ... + x{n} = {r} have?",
        f"You choose {num(rng, r)} scoops from {num(rng, n)} {f}, with repeats allowed and order irrelevant. How many selections are possible?",
        f"In how many ways can {num(rng, r)} identical balls be placed into {num(rng, n)} distinct bins?",
        f"A bakery has {num(rng, n)} types of {f.split()[0]} pastries. How many different boxes of {num(rng, r)} can be made, allowing multiples of the same type?",
        f"Using stars and bars, count the ways to give {num(rng, r)} identical {i} to {num(rng, n)} children.",
        f"How many multisets of size {num(rng, r)} can be formed from {num(rng, n)} distinct elements?",
        f"A customer picks {num(rng, r)} items from {num(rng, n)} {f}, and picking the same one more than once is fine. How many unordered choices exist?",
        f"How many ways can {num(rng, r)} donuts be selected from {num(rng, n)} varieties, if there are at least {num(rng, r)} of each variety?",
    ])


def circular_permutations(rng):
    n = rng.randint(3, 12)
    p, i = rng.choice(PEOPLE), rng.choice(ITEMS)
    return rng.choice([
        f"In how many ways can {num(rng, n)} {p} sit around a circular table?",
        f"How many ways can {num(rng, n)} distinct {i} be arranged on a round tray, if rotations count as the same arrangement?",
        f"{num(rng, n).capitalize()} {p} hold hands in a circle. How many different circles can be formed?",
        f"How many distinct necklaces can be made by threading {num(rng, n)} different beads, where rotations are considered identical?",
        f"Find the number of circular arrangements of {num(rng, n)} different {i}.",
        f"{num(rng, n).capitalize()} {p} are seated at a round banquet table. If rotating everyone gives the same seating, how many seatings exist?",
        f"In how many ways can {num(rng, n)} {p} stand in a ring around a campfire?",
        f"How many ways can {num(rng, n)} guests be seated around a circular dinner table when only relative positions matter?",
        f"A carousel has {num(rng, n)} different horses. How many ways can they be ordered around the carousel up to rotation?",
    ])


def derangements(rng):
    n = rng.randint(3, 12)
    p, i = rng.choice(PEOPLE), rng.choice(ITEMS)
    return rng.choice([
        f"{num(rng, n).capitalize()} {p} each leave a coat at a party and receive a random coat back. In how many ways can nobody get their own coat?",
        f"How many derangements are there of {num(rng, n)} objects?",
        f"A secretary puts {num(rng, n)} letters into {num(rng, n)} addressed envelopes at random. How many ways can every letter go into the wrong envelope?",
        f"{num(rng, n).capitalize()} {p} take part in a gift exchange where nobody may draw their own name. How many valid assignments exist?",
        f"In how many ways can {num(rng, n)} {i} be rearranged so that none ends up in its original position?",
        f"How many permutations of {num(rng, n)} distinct items leave no item in its original place?",
        f"{num(rng, n).capitalize()} {p} check in {num(rng, n)} hats. How many ways can the hats be returned so that nobody receives their own?",
        f"Count the arrangements of {num(rng, n)} numbered {i} in {num(rng, n)} numbered slots where no {i[:-1]} sits in the slot with its own number.",
        f"A teacher hands back {num(rng, n)} graded tests at random. In how many ways can every student receive someone else's test?",
        f"Secret Santa with {num(rng, n)} {p}: how many ways can gifts be assigned so that no one gives a gift to themselves?",
    ])


def permutations_with_replacement(rng):
    n, r = rng.randint(2, 10), rng.randint(2, 8)
    p, i = rng.choice(PEOPLE), rng.choice(ITEMS)
    return rng.choice([
        f"How many {num(rng, r)}-character passwords can be made from {num(rng, n)} symbols if symbols may repeat?",
        f"A lock has {num(rng, r)} dials, each showing one of {num(rng, n)} digits. How many different codes are possible?",
        f"In how many ways can {num(rng, r)} {p} each choose one of {num(rng, n)} {i}, if several may choose the same one?",
        f"How many {num(rng, r)}-letter strings can be written using an alphabet of {num(rng, n)} letters with repetition allowed?",
        f"A coin-like device has {num(rng, n)} states and is read {num(rng, r)} times. How many possible sequences of readings exist?",
        f"How many ordered sequences of length {num(rng, r)} can be formed from {num(rng, n)} choices when each position is chosen independently?",
        f"Each of {num(rng, r)} {p} is assigned one of {num(rng, n)} rooms, and rooms can hold any number of people. How many assignments are there?",
        f"How many different {num(rng, r)}-digit codes are possible if each digit is one of {num(rng, n)} values and digits can repeat?",
        f"A quiz has {num(rng, r)} questions, each with {num(rng, n)} possible answers. How many different answer sheets can be filled in?",
        f"How many words of length {num(rng, r)} can be made from {num(rng, n)} letters if any letter can be used any number of times?",
    ])


GENERATORS = {
    "permutations": permutations,
    "combinations": combinations,
    "combinations_with_replacement": combinations_with_replacement,
    "circular_permutations": circular_permutations,
    "derangements": derangements,
    "permutations_with_replacement": permutations_with_replacement,
}


def generate():
    rng = random.Random(SEED)
    held_out = set(pd.read_csv(os.path.join(_DIR, "eval_questions.csv"))["question"].str.lower())
    seen, rows = set(held_out), []
    for operation, make in GENERATORS.items():
        count = attempts = 0
        while count < PER_OPERATION and attempts < PER_OPERATION * 50:
            attempts += 1
            question = make(rng)
            if question.lower() in seen:
                continue
            seen.add(question.lower())
            rows.append((question, operation))
            count += 1
    return pd.DataFrame(rows, columns=["question", "operation"])


if __name__ == "__main__":
    df = generate()
    df.to_csv(os.path.join(_DIR, "train_generated.csv"), index=False)
    print(df["operation"].value_counts().to_string())
    print(f"[OK] Wrote {len(df)} rows to train_generated.csv")
