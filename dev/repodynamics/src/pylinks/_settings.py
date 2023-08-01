class Settings:
    def __init__(self):
        self._offline_mode = False
        return

    @property
    def offline_mode(self) -> bool:
        return self._offline_mode

    @offline_mode.setter
    def offline_mode(self, value: bool):
        self._offline_mode = bool(value)
        return


settings = Settings()
