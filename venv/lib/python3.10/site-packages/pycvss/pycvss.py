"""Pure python module to work with CVSS.

Usage:
  c = Cvss()
  # Build from enums:
  c.set(AV.network)
  c.set(E.functional)
  c.set(CDP.low)
  # Or from a vector:
  c = Cvss.from_vector("AV:N/CDP:L/E:F")
  # Get scores.
  c.to_vector()          # "AV:N/CDP:L/E:F"
  c.base_score           # 7.8
  c.temporal_score       # 6.4
  c.environmental_score  # 9.2

More details at:
http://www.first.org/cvss/cvss-guide
"""

import collections
import enum

# All enumerations are defined with their short name used in the vector
# declaration and their value when computing a score.
CvssEnumValue = collections.namedtuple("EnumValue", "short_name score")

@enum.unique
class AV(enum.Enum):
  """Access Vector."""
  local = CvssEnumValue("L", 0.395)
  adjacent = CvssEnumValue("A", 0.646)
  network = CvssEnumValue("N", 1.0)

@enum.unique
class AC(enum.Enum):
  """Access Complexity."""
  high = CvssEnumValue("H", 0.35)
  medium = CvssEnumValue("M", 0.61)
  low = CvssEnumValue("L", 0.71)

@enum.unique
class Au(enum.Enum):
  """Authentication."""
  multiple = CvssEnumValue("M", 0.45)
  single = CvssEnumValue("S", 0.56)
  none = CvssEnumValue("N", 0.704)

@enum.unique
class C(enum.Enum):
  """Confidentiality Impact."""
  none = CvssEnumValue("N", 0.0)
  partial = CvssEnumValue("P", 0.275)
  complete = CvssEnumValue("C", 0.660)

@enum.unique
class I(enum.Enum):
  """Integrity Impact."""
  none = CvssEnumValue("N", 0.0)
  partial = CvssEnumValue("P", 0.275)
  complete = CvssEnumValue("C", 0.660)

@enum.unique
class A(enum.Enum):
  """Availability impact."""
  none = CvssEnumValue("N", 0.0)
  partial = CvssEnumValue("P", 0.275)
  complete = CvssEnumValue("C", 0.660)

@enum.unique
class E(enum.Enum):
  """Exploitability."""
  unproven = CvssEnumValue("U", 0.85)
  proof_of_concept = CvssEnumValue("POC", 0.9)
  functional = CvssEnumValue("F", 0.95)
  high = CvssEnumValue("H", 1.0)
  not_defined = CvssEnumValue("ND", 1.0)

@enum.unique
class RL(enum.Enum):
  """Remediation Level."""
  official_fix = CvssEnumValue("OF", 0.87)
  temporary_fix = CvssEnumValue("TF", 0.9)
  workaround = CvssEnumValue("W", 0.95)
  unavailable = CvssEnumValue("U", 1.0)
  not_defined = CvssEnumValue("ND", 1.0)

@enum.unique
class RC(enum.Enum):
  """Report Confidence."""
  unconfirmed = CvssEnumValue("UC", 0.9)
  uncorroborated = CvssEnumValue("UR", 0.95)
  confirmed = CvssEnumValue("C", 1.0)
  not_defined = CvssEnumValue("ND", 1.0)

@enum.unique
class CDP(enum.Enum):
  """Collateral Damage Potential."""
  none = CvssEnumValue("N", 0.0)
  low = CvssEnumValue("L", 0.1)
  low_medium = CvssEnumValue("LM", 0.3)
  medium_high = CvssEnumValue("MH", 0.4)
  high = CvssEnumValue("H", 0.5)
  not_defined = CvssEnumValue("ND", 0.0)

@enum.unique
class TD(enum.Enum):
  """Target Distribution."""
  none = CvssEnumValue("N", 0.0)
  low = CvssEnumValue("L", 0.25)
  medium = CvssEnumValue("M", 0.75)
  high = CvssEnumValue("H", 1.0)
  not_defined = CvssEnumValue("ND", 1.0)

@enum.unique
class CR(enum.Enum):
  """Confidentiality Requirement."""
  low = CvssEnumValue("L", 0.5)
  medium = CvssEnumValue("M", 1.0)
  high = CvssEnumValue("H", 1.51)
  not_defined = CvssEnumValue("ND", 1.0)

@enum.unique
class IR(enum.Enum):
  """Integrity Requirement."""
  low = CvssEnumValue("L", 0.5)
  medium = CvssEnumValue("M", 1.0)
  high = CvssEnumValue("H", 1.51)
  not_defined = CvssEnumValue("ND", 1.0)

@enum.unique
class AR(enum.Enum):
  """Availability Requirement."""
  low = CvssEnumValue("L", 0.5)
  medium = CvssEnumValue("M", 1.0)
  high = CvssEnumValue("H", 1.51)
  not_defined = CvssEnumValue("ND", 1.0)

_base_vector = (AV, AC, Au, C, I, A)
_temporal_vector = (E, RL, RC)
_environmental_vector = (CDP, TD, CR, IR, AR)

_NAME_TO_ENUM = {e.__name__: e for e in
                 _base_vector + _temporal_vector + _environmental_vector}


class Cvss(object):
  """Common Vulnerability Scoring System.

  Use this class to set base, temporal and environmental vectors and
  compute scores.
  Cf module level documentation for sample usage.
  """

  _BASE_VECTOR = (AV, AC, Au, C, I, A)
  _TEMPORAL_VECTOR = (E, RL, RC)
  _ENVIRONMENTAL_VECTOR = (CDP, TD, CR, IR, AR)
  _ALL_VECS = set(_BASE_VECTOR + _TEMPORAL_VECTOR + _ENVIRONMENTAL_VECTOR)

  def __init__(self):
    self._vectors = set()

  def set(self, vec):
    """Adds a vector to this CVSS, no-op if already present.

    Args:
      - vec: Any of the CVSS enum values.

    Raises:
      - ValueError: If the passed vec is not a valid cvss enum value.
    """
    for val in self._ALL_VECS:
      if vec in val:
        # First remove any other value already present.
        for maybe_existing in val:
          if maybe_existing in self._vectors:
            self._vectors.remove(maybe_existing)
        # Then add our vector.
        self._vectors.add(vec)
        return
    raise ValueError("Vector %s not a valid Cvss enum." % vec)

  def unset(self, vec):
    """Removes a vector from this CVSS, no-op if not present.

    Args:
      - vec: Any of the CVSS enum values.
    """
    if vec in self._vectors:
      self._vectors.remove(vec)
      return

  def has(self, vec):
    """Returns True if the current construct has the given vector."""
    return vec in self._vectors

  @classmethod
  def from_vector(cls, vector):
    """Creates a Cvss from the given vector.

    For example, a vulnerability with base metric values of
    "Access Vector: Low, Access Complexity: Medium,
    Authentication: None, Confidentiality Impact: None,
    Integrity Impact: Partial, Availability Impact: Complete"
    would have the following base vector: "AV:L/AC:M/Au:N/C:N/I:P/A:C."

    Args:
      - vector: A string in the form defined by the cvss spec:
      "Each metric in the vector consists of the abbreviated metric name,
      followed by a ":" (colon), then the abbreviated metric value.
      The vector lists these metrics in a predetermined order, using
      the "/" (slash) character to separate the metrics.
    Raises:
      - ValueError: If the vector contains invalid enum names or values.

    Returns:
      A new Cvss instance parsed from the vector.
    """

    cvss_repr = Cvss()
    for pair in vector.split("/"):
      enum_short_name, enum_val = pair.split(":")
      cvss_enum = _NAME_TO_ENUM[enum_short_name]
      for val in cvss_enum:
        if val.value.short_name == enum_val:
          cvss_repr.set(val)
          break
      else:
        raise ValueError("%s is not a valid enum value" % enum_val)
    return cvss_repr

  def to_vector(self):
    """Converts the current Cvss instance to a string vector."""
    vec = []
    for base in self._vectors:
      vec.append(base.__class__.__name__ + ":" + base.value.short_name)
    # Make it sorted to be predictable and consistent.
    return "/".join(sorted(vec))

  @property
  def base_score(self):
    return self._get_base_score(self.impact, self.impact_mod)

  def _get_base_score(self, impact, impact_mod):
    return round(
        ((0.6 * impact) + (0.4 * self.base_exploitability) - 1.5) * impact_mod,
        1)

  @property
  def impact(self):
    return 10.41 * (
        1.0 - (1.0 - self.confidentiality_impact) *
              (1.0 - self.integrity_impact) *
              (1.0 - self.availability_impact))

  @property
  def base_exploitability(self):
    return (20.0 *
        self.access_vector_score *
        self.access_complexity_score *
        self.authentication_score)

  @property
  def impact_mod(self):
    return 0.0 if self.impact == 0.0 else 1.176

  @property
  def access_vector_score(self):
    for val in AV:
      if val in self._vectors:
        return val.value.score
    return 0.0

  @property
  def access_complexity_score(self):
    for val in AC:
      if val in self._vectors:
        return val.value.score
    return 0.0

  @property
  def authentication_score(self):
    for val in Au:
      if val in self._vectors:
        return val.value.score
    return 0.0

  @property
  def confidentiality_impact(self):
    for val in C:
      if val in self._vectors:
        return val.value.score
    return 0.0

  @property
  def integrity_impact(self):
    for val in I:
      if val in self._vectors:
        return val.value.score
    return 0.0

  @property
  def availability_impact(self):
    for val in A:
      if val in self._vectors:
        return val.value.score
    return 0.0

  @property
  def temporal_score(self):
    return self._get_temporal_score(self.base_score)

  def _get_temporal_score(self, base_score):
    return round(
        base_score *
        self.temporal_exploitability *
        self.remediation_level *
        self.report_confidence,
        1)

  @property
  def temporal_exploitability(self):
    for val in E:
      if val in self._vectors:
        return val.value.score
    return E.not_defined.value.score

  @property
  def remediation_level(self):
    for val in RL:
      if val in self._vectors:
        return val.value.score
    return RL.not_defined.value.score

  @property
  def report_confidence(self):
    for val in RC:
      if val in self._vectors:
        return val.value.score
    return RC.not_defined.value.score

  @property
  def environmental_score(self):
    return round(
        (self.adjusted_temporal + (10 - self.adjusted_temporal) *
            self.collateral_damage_potential) * self.target_distribution,
        1)

  @property
  def adjusted_temporal(self):
    return self._get_temporal_score(
        self._get_base_score(self.adjusted_impact, self.adjusted_impact_mod))

  @property
  def adjusted_impact(self):
    return min(
        10,
        10.41 * (1 - (1- self.confidentiality_impact * self.confidentiality_requirement) *
            (1 - self.integrity_impact * self.integrity_requirement) *
            (1 - self.availability_impact * self.availability_requirement)))

  @property
  def adjusted_impact_mod(self):
    return 0.0 if self.adjusted_impact == 0.0 else 1.176

  @property
  def collateral_damage_potential(self):
    for val in CDP:
      if val in self._vectors:
        return val.value.score
    return CDP.not_defined.value.score

  @property
  def target_distribution(self):
    for val in TD:
      if val in self._vectors:
        return val.value.score
    return TD.not_defined.value.score

  @property
  def confidentiality_requirement(self):
    for val in CR:
      if val in self._vectors:
        return val.value.score
    return CR.not_defined.value.score

  @property
  def integrity_requirement(self):
    for val in IR:
      if val in self._vectors:
        return val.value.score
    return IR.not_defined.value.score

  @property
  def availability_requirement(self):
    for val in AR:
      if val in self._vectors:
        return val.value.score
    return AR.not_defined.value.score

  def __repr__(self):
    return (
        "{}\n"
        "base score                     {}\n"
        "  access vector                {}\n"
        "  access complexity            {}\n"
        "  authentication               {}\n"
        "  confidentiality impact       {}\n"
        "  integrity impact             {}\n"
        "  availability impact          {}\n"
        "\n"
        "temporal score                 {}\n"
        "  exploitability               {}\n"
        "  remediation level            {}\n"
        "  report confidence            {}\n"
        "\n"
        "environmental score            {}\n"
        "  collateral damage potential  {}\n"
        "  target distribution          {}\n"
        "  confidentiality requirement  {}\n"
        "  integrity requirement        {}\n"
        "  availability requirement     {}\n"
        "".format(
            self.to_vector(),
            self.base_score,
            self.access_vector_score,
            self.access_complexity_score,
            self.authentication_score,
            self.confidentiality_impact,
            self.integrity_impact,
            self.availability_impact,

            self.temporal_score,
            self.temporal_exploitability,
            self.remediation_level,
            self.report_confidence,

            self.environmental_score,
            self.collateral_damage_potential,
            self.target_distribution,
            self.confidentiality_requirement,
            self.integrity_requirement,
            self.availability_requirement,
    ))
