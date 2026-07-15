from sample_order_system.model.sample import Sample
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.view import sample_view


class SampleController:
    """시료 관리(등록/조회/검색) 흐름을 담당."""

    def __init__(self, sample_repository: SampleRepository):
        self.sample_repository = sample_repository

    def run(self) -> None:
        while True:
            sample_view.show_sample_menu()
            choice = sample_view.get_sample_menu_choice()
            if choice == "1":
                self.register_sample()
            elif choice == "2":
                self.list_samples()
            elif choice == "3":
                self.search_sample()
            elif choice == "0":
                break

    def register_sample(self) -> None:
        data = sample_view.get_new_sample_input()
        try:
            self.sample_repository.create(Sample(**data))
        except ValueError as e:
            sample_view.show_error(str(e))

    def list_samples(self) -> None:
        sample_view.show_sample_list(self.sample_repository.list_all())

    def search_sample(self) -> None:
        keyword = sample_view.get_search_keyword()
        sample_view.show_search_result(self.sample_repository.search(keyword))
