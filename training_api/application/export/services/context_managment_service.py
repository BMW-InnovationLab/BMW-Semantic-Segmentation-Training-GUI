import mxnet as mx
from mxnet import Context
from typing import List

from domain.services.contracts.abstract_memory_context_managment import AbstractContextManagementService


class ContextManagementService(AbstractContextManagementService):
    def __get_ctx(self, gpus_list) -> List[Context]:
        gpu_count: int = mx.util.get_gpu_count()
        if gpu_count > 0:
            ctx = [mx.gpu(gpu) for gpu in gpus_list] if gpus_list[0] != -1 else [mx.cpu(0)]
        else:
            ctx = [mx.cpu(0)]
        return ctx

    def clean_context(self, gpus_list: List[int]) -> None:
        ctx_list: List[Context] = self.__get_ctx(gpus_list=gpus_list)
        for ctx in ctx_list:
            ctx.empty_cache()
