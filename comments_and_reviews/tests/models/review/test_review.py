from dataclasses import asdict

from app.models.Review import Status


def test_metadata_touch(metadata):
    prev_edited_at = metadata.edited_at
    metadata.touch()
    assert prev_edited_at < metadata.edited_at


class TestReview:
    def test_to_dict(self, review, content):
        assert review.to_dict() == {
            "id": review.id,
            "author": review.author.to_dict(),
            "status": review.status,
            "content": asdict(content),
            "answer": review.answer,
            "likes": review.likes,
            "metadata": asdict(review.metadata),
        }


class TestReviewForSeller:
    def test_add_answer(self, review_for_seller, answer):
        review_for_seller.add_answer(answer)
        assert review_for_seller.answer == answer

    def test_to_moderation(self, review_for_seller):
        review_for_seller.to_moderation()
        assert review_for_seller.status == Status.PENDING


class TestRevewForAuthor:
    def test_update(self, review_for_author, content):
        review_for_author.update(content)
        assert review_for_author.content == content
        assert review_for_author.status == Status.PENDING


class TestReviewForBuyer:
    def test_like(self, review_for_buyer):
        review_for_buyer.like()
        assert review_for_buyer.likes == 1

    def test_unlike(self, review_for_buyer):
        review_for_buyer.unlike()
        assert review_for_buyer.likes == 0

    def test_unlike_nonzero_likes(self, review_for_buyer):
        review_for_buyer.likes = 1
        review_for_buyer.unlike()
        assert review_for_buyer.likes == 0


class TestReviewForModerator:
    def test_hide(self, review_for_moderator):
        review_for_moderator.hide()
        assert review_for_moderator.status == Status.HIDDEN

    def test_publish(self, review_for_moderator):
        review_for_moderator.publish()
        assert review_for_moderator.status == Status.PUBLISHED
