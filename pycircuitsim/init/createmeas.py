from pycircuitsim.impl.measurableimpl import MeasurableImpl


def create_meas(name: str):
    return MeasurableImpl(name=name)
