from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    async def list(self) -> List[T]:
        pass

    @abstractmethod
    async def add(self, obj: T) -> T:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass