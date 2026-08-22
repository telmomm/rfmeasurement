from rfmeasurement.domain.enums import Distribution, UncertaintyType
from rfmeasurement.domain.measurand import Measurand
from rfmeasurement.domain.uncertainty import UncertaintySource
from rfmeasurement.domain.uncertainty_model import UncertaintyModel


def test_uncertainty_model_holds_function_and_assumptions():
    source = UncertaintySource(
        name="x",
        description="test",
        uncertainty_type=UncertaintyType.TYPE_B,
        distribution=Distribution.NORMAL,
        standard_uncertainty=0.1,
        unit="linear",
        nominal_value=1.0,
    )
    model = UncertaintyModel(
        measurand=Measurand(name="y", definition="identity of x", unit="linear"),
        function=lambda values: values["x"],
        sources=(source,),
        assumptions="y equals x exactly; no other error sources considered.",
    )
    assert model.function({"x": 2.0}) == 2.0
    assert model.sensitivity is None
    assert model.sources == (source,)
