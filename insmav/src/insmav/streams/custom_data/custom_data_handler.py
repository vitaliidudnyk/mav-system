from insmav.streams.custom_data.custom_data_sets import DatasetType, DATASET_TYPES
from insmav.streams.shared.base_handler import BaseHandler


class DatasetHandler(BaseHandler):
    def __init__(self, state):
        self._state = state

    @property
    def message_type(self) -> str:
        return "DEBUG_FLOAT_ARRAY"

    def handle(self, message) -> None:
        raw_name = self._extract_name(message)

        try:
            dataset_type = DatasetType(raw_name)
        except ValueError:
            print(
                f"[Dataset][unknown] "
                f"name={raw_name} "
                f"array_id={message.array_id} "
                f"data={list(message.data)}"
            )
            return

        dataset_class = DATASET_TYPES.get(dataset_type)

        if dataset_class is None:
            print(
                f"[Dataset][unmapped] "
                f"dataset_type={dataset_type.value} "
                f"array_id={message.array_id} "
                f"data={list(message.data)}"
            )
            return

        dataset = dataset_class.from_array(list(message.data))

        # print(
        #     f"[Dataset][parsed] "
        #     f"dataset_type={dataset_type.value} "
        #     f"array_id={message.array_id} "
        #     f"dataset={dataset}"
        # )

        self._state.add_dataset(dataset_type.value, dataset)

    def _extract_name(self, message) -> str:
        raw_name = message.name

        if isinstance(raw_name, bytes):
            return raw_name.decode("utf-8", errors="ignore").rstrip("\x00").strip()

        return str(raw_name).rstrip("\x00").strip()