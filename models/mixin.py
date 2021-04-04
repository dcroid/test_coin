MAX_LIMIT = 5


class SortedMixin:
    @staticmethod
    def lim_sorted(data):
        result = data[:MAX_LIMIT]
        result = sorted(result, key=lambda i: i.ask)
        return result