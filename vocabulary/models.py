from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

User = get_user_model()


class WordList(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_last_opened = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="word_lists"
    )

    class Meta:
        verbose_name = "Word list"
        verbose_name_plural = "Word lists"
        ordering = ["title"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "user"],
                name="unique_title_user"
            )
        ]

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tags"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="unique_name_user"
            )
        ]


class PartOfSpeech(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(unique=True)

    class Meta:
        verbose_name = "Part of speech"
        verbose_name_plural = "Parts of speech"
        ordering = ["id"]

    def __str__(self):
        return self.name


class KnowledgeLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(unique=True)

    class Meta:
        verbose_name = "Knowledge level"
        verbose_name_plural = "Knowledge levels"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Word(models.Model):
    part_of_speech = models.ForeignKey(
        PartOfSpeech,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="words"
    )
    text = models.CharField(max_length=255, unique=True)
    transcription = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    knowledge_level = models.ForeignKey(
        KnowledgeLevel,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="words"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        through="WordTag",
        related_name="words"
    )
    word_lists = models.ManyToManyField(
        WordList,
        through="WordWordList",
        related_name="words"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="words"
    )

    class Meta:
        ordering = ["date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["part_of_speech", "text", "user"],
                name="unique_part_of_speech_word_user"
            )
        ]

    def __str__(self):
        part_of_speech_str = (
            self.part_of_speech.short_name
            if self.part_of_speech
            else "n/a"
        )
        translations_list = list(self.translations.all())
        translation_str = (
            translations_list[0].translation
            if translations_list
            else "n/a"
        )
        if len(translations_list) > 1:
            translation_str += f" (+{len(translations_list) - 1})"

        return (
            f"({part_of_speech_str}) {self.text} /{self.transcription}/ "
            f"- {translation_str}"
        )


class WordWordList(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    word_list = models.ForeignKey(WordList, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["word", "word_list"],
                name="unique_word_word_list"
            )
        ]


class WordTag(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["word", "tag"],
                name="unique_word_tag"
            )
        ]


class Translation(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="translations"
    )
    text = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["word", "text"],
                name="unique_word_translation"
            )
        ]


class Definition(models.Model):
    word = models.ForeignKey(
        Word,
        on_delete=models.CASCADE,
        related_name="definitions"
    )
    text = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["word", "text"],
                name="unique_word_definition"
            )
        ]


class Example(models.Model):
    definition = models.ForeignKey(
        Definition,
        on_delete=models.CASCADE,
        related_name="examples"
    )
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["definition", "text"],
                name="unique_definition_example"
            )
        ]
