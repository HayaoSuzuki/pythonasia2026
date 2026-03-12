# Presentation Script: "Let's implement useless Python objects"

**Event:** PythonAsia 2026, March 21, 2026, Manila
**Duration:** 30 minutes
**Speaker:** Hayao Suzuki

> Note: `[Pause]` means take a short breath (1-2 seconds). `[Long Pause]` means wait 3-4 seconds to let the audience think.

---

## Slide 1: Title Page (0:00 - 0:30) ~30s

Hello everyone. Thank you for coming today.

My name is Hayao Suzuki.

Today, I will talk about "Let's implement useless Python objects."

---

## Slide 2: Share it (0:30 - 1:00) ~30s

Before we start, let me share some links.

The slides and code are on GitHub. The URL is on the screen.

If you want to share on social media, please use the hashtag #PythonAsia2026.

---

## Slide 3: Who am I? - Name & Work (1:00 - 1:40) ~40s

Let me introduce myself quickly.

My name is Hayao Suzuki. You can find me on X as follows.

I work as a software engineer at Tokyo Gas. Tokyo Gas is the largest natural gas company in Japan. We provide city gas, LNG, and electricity.

---

## Slide 4: Who am I? - Books (1:40 - 2:20) ~40s

I translate Python books into Japanese.

Recently, I translated "Effective Python, Third Edition" for O'Reilly Japan. This is the newest one.

I also translated "Hypermodern Python" and "Python Distilled."

And I supervised the Japanese editions of "Robust Python," "Introducing Python," and "Python in a Nutshell."

---

## Slide 5: Who am I? - Presentations (2:20 - 3:00) ~40s

I have given many talks at PyCon events.

Actually, I gave a similar talk at PyCon APAC 2023. Today's version is updated for PythonAsia.

You can find all my past talks on my blog. The URL is on the slide.

OK, that's enough about me. Let's get started!

---

## Slide 6: Today's Theme (3:00 - 3:40) ~40s

Today's theme is:

"Let's implement **useless** Python objects."

[Long Pause]

The keyword here is "useless." What does that mean? And why should we care?

Let me explain.

---

## Slide 7: What does "useless" mean? (3:40 - 5:20) ~100s

So, what does "useless" mean?

I looked it up in the Longman Dictionary.

[Pause]

The first meaning is: "not useful or effective in any way."

The second meaning is more informal: "unable or unwilling to do anything properly."

[Pause]

Today, we will make Python objects that match these definitions. They look normal. They have the right methods. They pass type checks. But... they don't work properly.

[Pause]

For example, imagine a container. You put "spam" inside. Then you ask "Is spam in the container?" And it says "No." That is a useless object.

Sounds fun, right?

---

## Slide 8: Is the useless object really useless? (5:20 - 7:40) ~140s

But wait. Is "useless" really useless?

[Pause]

Let me show you a quote. This is from Zhuangzi, an ancient Chinese philosopher. He lived about 2,300 years ago.

[Pause]

The quote says:

"Everyone knows the usefulness of the useful, but no one knows the usefulness of the useless."

[Long Pause]

This is a very deep idea. Let me explain.

In Zhuangzi's story, there is a big tree. The tree is so twisted and bent that no carpenter can use it. People say it is "useless."

But because the tree is useless, nobody cuts it down. The tree lives for hundreds of years. So being "useless" actually saved the tree.

[Pause]

I think the same idea applies to programming.

When we try to make something "useless," we must deeply understand how things work. We need to know the rules first. Then we can break them in a funny way.

[Pause]

So making useless things is actually a very good way to learn. The useless teaches us about the useful.

---

## Slide 9: Today's Theme - Key Message (7:40 - 9:00) ~80s

And this is the key message of today's talk.

[Pause]

Please read the slide with me:

"The useless objects are useless, but **how to make a useless object** is very useful."

[Long Pause]

The process of making useless objects teaches us important things. We will learn about object protocols. We will learn about abstract base classes. We will learn how Python works inside.

[Pause]

The goal is not the useless object itself. The goal is learning through the process of making it.

Remember this idea. Let's keep it in mind as we go through the examples.

---

## Slide 10: LiarContainer Example (9:00 - 9:45) ~45s

OK, let me show you some examples of useless objects.

First is LiarContainer.

You create it with a list: "spam", "egg", "bacon."

Then you ask: is "spam" in the container? It says False.

Is "tomato" in the container? It says True.

[Pause]

It always lies! That's why it's called LiarContainer.

---

## Slide 11: FibonacciSized Example (9:45 - 10:15) ~30s

Next is FibonacciSized.

You create it with range(50). So it has 50 items.

But when you call len(), it returns... 12 billion!

It returns a Fibonacci number instead of the real length.

---

## Slide 12: ShuffledIterable Example (10:15 - 10:50) ~35s

And this is ShuffledIterable.

You create it with [1, 2, 3, 4, 5].

Every time you loop over it with `for`, the order changes.

Look: first time, 5 3 4 2 1. Second time, 4 1 2 3 5. Third time, 2 5 3 1 4.

You never get the same order twice!

---

## Slide 13: Definition (10:50 - 12:00) ~70s

So, what is a "useless Python object"? Let me give a definition.

[Pause]

"A useless Python object behaves **Pythonic**, but does not work as expected."

[Long Pause]

This is important. The object follows Python's rules. It has the right methods. It has the right interface. But the behavior is wrong.

[Pause]

To make such an object, we need to understand what "Pythonic" really means. What is the correct interface? What methods do we need?

That's what we will explore in the rest of this talk.

---

## Slide 14: Data Structures and Operations (12:00 - 14:00) ~120s

Let's start with Python's basic data structures.

Python has four main data structures: List, Tuple, Dictionary, and Set. You all use them every day.

[Pause]

These data structures share common operations.

`len()` gives you the length. The `in` operator tests membership. `for` lets you iterate.

[Pause]

Have you ever wondered: how does Python know what to do? How does `len()` work on both a list and a dictionary?

[Long Pause]

The answer is: **object protocols**.

Each operation uses a special method. `len()` calls `__len__`. `in` calls `__contains__`. `for` calls `__iter__`.

These are called "dunder methods" — double underscore methods.

If we define these methods, we can make our own objects work with `len()`, `in`, and `for`. And if we change these methods... we can make useless objects.

Let me show you how.

---

## Slide 15: `in` and Container (14:00 - 15:20) ~80s

First, the `in` operator and the Container class.

The `__contains__` method is called for membership testing.

[Pause]

Look at LiarContainer. It inherits from Container.

The `__contains__` method has just one line: `return item not in self._data`.

See the word `not`? It flips the result.

If the item is in the data, it returns False. If the item is NOT in the data, it returns True.

[Pause]

One line of code makes it completely useless. Simple and fun.

---

## Slide 16: `len()` and Sized (15:20 - 16:20) ~60s

Next, `len()` and the Sized class.

The `__len__` method is called for the built-in `len()` function.

[Pause]

FibonacciSized inherits from Sized.

Instead of returning the real length, it calculates a Fibonacci number. It uses the golden ratio formula — PHI to the power of the real length.

So if your data has 50 items, `len()` returns the 50th Fibonacci number. That's 12 billion!

---

## Slide 17: `for` and Iterable (16:20 - 17:20) ~60s

And the `for` loop with the Iterable class.

The `__iter__` method is called when you use a for loop.

[Pause]

ShuffledIterable inherits from Iterable.

In `__iter__`, it uses `random.sample` to shuffle all items. It returns a new random order every time.

[Pause]

So now we have three basic useless objects. Each one breaks one operation. Let's go deeper.

---

## Slide 18: Object Protocols (17:20 - 17:50) ~30s

To make useless objects, we first need to understand **object protocols**.

Object protocols are the rules for how Python objects should behave. You can read the full details in the Python Data Model reference. The URL is on the slide.

---

## Slide 19: collections.abc (17:50 - 18:20) ~30s

And Python gives us a very useful tool: the `collections.abc` module.

This module provides **abstract base classes**. They define the interface for different types of collections.

We already used Container, Sized, and Iterable. These all come from `collections.abc`.

---

## Slide 20: collections.abc - Table (18:20 - 19:00) ~40s

Here is a summary table.

Sized needs `__len__`. Container needs `__contains__`. Iterable needs `__iter__`.

And Collection combines all three.

[Pause]

If your class inherits from Collection, it must have `__len__`, `__contains__`, and `__iter__`. Then Python knows your class is a collection.

---

## Slide 21: Collection - UselessCollection (19:00 - 19:40) ~40s

So we can combine our useless classes!

Look at UselessCollection. It inherits from FibonacciSized, LiarContainer, and ShuffledIterable.

The class body is just `pass`. We don't need any new code!

[Pause]

Python's multiple inheritance does the work. Three useless classes become one super-useless collection. This is the power of abstract base classes.

---

## Slide 22: collections.abc - Built-in Objects (19:40 - 20:10) ~30s

Now let's go further.

`collections.abc` also defines ABCs for built-in types.

Sequence matches tuple. MutableSequence matches list. MutableSet matches set. MutableMapping matches dict.

Let's implement some more useless objects using these.

---

## Slide 23: Sequence - ModularSequence code (20:10 - 21:10) ~60s

This is ModularSequence. It inherits from Sequence.

The key method is `__getitem__`. This is called when you use square brackets, like `seq[5]`.

[Pause]

Look at the code. When you access an index, it uses modular arithmetic: `key % len(self._data)`.

So the index wraps around. If the data has 20 items, index 0 and index 20 give the same result. Index 21 is the same as index 1.

The same logic applies to slices.

---

## Slide 24: Sequence - ModularSequence demo (21:10 - 22:10) ~60s

Let me show you what happens.

Create a ModularSequence with range(20). It has items 0 to 19.

`seq[21:44]` returns [1, 2, 3]. The indices wrap around.

`seq[65543]` returns 3. Because 65543 mod 20 is 3.

[Pause]

And here is a fun bug. If you call `seq.count(13)`, it **never stops**.

Why? Because Sequence provides `count()` for free. But `count()` checks every index from 0, 1, 2, ... And our sequence has no end — every index wraps around and gives a valid result. So it loops forever!

This is a great example of an unexpected side effect.

---

## Slide 25: Mapping - MisprintedDictionary code (22:10 - 23:00) ~50s

Next is MisprintedDictionary. It inherits from Mapping.

In `__init__`, it takes a normal dictionary. Then it shuffles the keys and values **separately**. And creates a new dictionary with random key-value pairs.

So the keys are the same. But the values are mixed up. Like a misprinted book where the pages are in the wrong order.

---

## Slide 26: Mapping - MisprintedDictionary demo (23:00 - 23:40) ~40s

Look at this example.

You create it with `{"a": 1, "b": 2, "c": 3}`.

When you iterate, you get: `d[c]=1`, `d[b]=2`, `d[a]=3`.

The keys and values are all mixed up. You can never trust what you get back!

---

## Slide 27: Set - CrowdSet code (23:40 - 24:30) ~50s

The last example is CrowdSet. It inherits from Set.

It also uses `functools.total_ordering`.

[Pause]

The trick is in `__lt__` — the less-than method.

Instead of checking `self._data <= other`, it checks `self._data >= other`.

The comparison is reversed! Bigger sets are "less than" smaller sets.

---

## Slide 28: Set - CrowdSet demo (24:30 - 25:10) ~40s

Here is the result.

`s` has 3 unique items: "egg", "bacon", "spam."
`t` has 2 unique items: "egg" and "spam." Remember, sets remove duplicates.

`s > t` returns True. But with CrowdSet's reversed logic, this means s has **more** elements.

It's called CrowdSet because the more crowded set thinks it is smaller.

---

## Slide 29: Conclusion (25:10 - 27:00) ~110s

Let me wrap up.

[Long Pause]

Three things to remember.

[Pause]

**First:** Useless Python objects are useful. The process of making them teaches us about Python.

[Pause]

**Second:** The `collections.abc` module is very useful. It gives us abstract base classes for all kinds of collections.

[Pause]

**Third:** Once you understand object protocols, you can do anything. You can make normal objects. You can make useless objects. You understand how Python really works.

[Long Pause]

Remember the Zhuangzi quote:

"Everyone knows the usefulness of the useful, but no one knows the usefulness of the useless."

[Pause]

I hope this talk inspires you to try making your own useless objects. It is a fun way to learn Python deeply.

Thank you very much!

---

## Q&A (27:00 - 30:00) ~3min

Are there any questions?

---

## Time Summary

| Section | Slides | Time |
|---|---|---|
| Title & Share | 1-2 | 1 min |
| Self Introduction | 3-5 | 2 min |
| What is "useless" & why it matters | 6-9 | 6 min |
| Useless Python object examples | 10-13 | 3 min |
| Data Structures & Operations | 14 | 2 min |
| Container / Sized / Iterable | 15-17 | 3.5 min |
| Object Protocols & collections.abc | 18-21 | 2.5 min |
| Sequence / Mapping / Set | 22-28 | 5.5 min |
| Conclusion | 29 | 2 min |
| Q&A / Buffer | - | 3 min |
| **Total** | **29 slides** | **~30 min** |
