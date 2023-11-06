import unittest

from pycvss.pycvss import *

class TestPyCvss(unittest.TestCase):

  def test_cve_2002_0392_high_env(self):
    c = Cvss.from_vector("AV:N/AC:L/Au:N/C:N/I:N/A:C")
    # temp
    c.set(E.functional)
    c.set(RL.official_fix)
    c.set(RC.confirmed)
    # env
    c.set(CDP.high)
    c.set(TD.high)
    c.set(CR.medium)
    c.set(IR.medium)
    c.set(AR.high)

    self.assertEqual(7.8, c.base_score)
    self.assertEqual(6.4, c.temporal_score)
    self.assertEqual(9.2, c.environmental_score)

  def test_cve_2002_0392_low_env(self):
    c = Cvss.from_vector("AV:N/AC:L/Au:N/C:N/I:N/A:C")
    # temp
    c.set(E.functional)
    c.set(RL.official_fix)
    c.set(RC.confirmed)
    # env
    c.set(CDP.none)
    c.set(TD.none)
    c.set(CR.medium)
    c.set(IR.medium)
    c.set(AR.high)

    self.assertEqual(7.8, c.base_score)
    self.assertEqual(6.4, c.temporal_score)
    self.assertEqual(0.0, c.environmental_score)

  def test_cve_2003_0818_high_env(self):
    c = Cvss.from_vector("AV:N/AC:L/Au:N/C:C/I:C/A:C")
    # temp
    c.set(E.functional)
    c.set(RL.official_fix)
    c.set(RC.confirmed)
    # env
    c.set(CDP.high)
    c.set(TD.high)
    c.set(CR.medium)
    c.set(IR.medium)
    c.set(AR.low)

    self.assertEqual(10.0, c.base_score)
    self.assertEqual(8.3, c.temporal_score)
    self.assertEqual(9.0, c.environmental_score)

  def test_cve_2003_0818_low_env(self):
    c = Cvss.from_vector("AV:N/AC:L/Au:N/C:C/I:C/A:C")
    # temp
    c.set(E.functional)
    c.set(RL.official_fix)
    c.set(RC.confirmed)
    # env
    c.set(CDP.none)
    c.set(TD.none)
    c.set(CR.medium)
    c.set(IR.medium)
    c.set(AR.low)

    self.assertEqual(10.0, c.base_score)
    self.assertEqual(8.3, c.temporal_score)
    self.assertEqual(0.0, c.environmental_score)

  def test_cve_2003_0062_high_env(self):
    c = Cvss.from_vector("AV:L/AC:H/Au:N/C:C/I:C/A:C")
    # temp
    c.set(E.proof_of_concept)
    c.set(RL.official_fix)
    c.set(RC.confirmed)
    # env
    c.set(CDP.high)
    c.set(TD.high)
    c.set(CR.medium)
    c.set(IR.medium)
    c.set(AR.medium)

    self.assertEqual(6.2, c.base_score)
    self.assertEqual(4.9, c.temporal_score)
    self.assertEqual(7.5, c.environmental_score)

  def test_cve_2003_0062_low_env(self):
    c = Cvss.from_vector("AV:L/AC:H/Au:N/C:C/I:C/A:C")
    # temp
    c.set(E.proof_of_concept)
    c.set(RL.official_fix)
    c.set(RC.confirmed)
    # env
    c.set(CDP.none)
    c.set(TD.none)
    c.set(CR.medium)
    c.set(IR.medium)
    c.set(AR.medium)

    self.assertEqual(6.2, c.base_score)
    self.assertEqual(4.9, c.temporal_score)
    self.assertEqual(0.0, c.environmental_score)

  def test_from_and_to_vector(self):
    vec = "A:C/AC:H/AV:L/Au:N/C:C/I:C"
    c = Cvss.from_vector(vec)
    self.assertEqual(vec, c.to_vector())

  def test_from_vector_raises(self):
    self.assertRaises(
        ValueError, Cvss.from_vector, "not a valid enum")
    self.assertRaises(
        ValueError, Cvss.from_vector, "C:not a valid value")

  def test_set_unset(self):
    c = Cvss()
    c.set(AV.network)
    c.set(E.functional)
    c.set(CDP.low)
    self.assertEqual("AV:N/CDP:L/E:F", c.to_vector())
    c.unset(AV.network)
    c.unset(E.functional)
    c.unset(CDP.low)
    self.assertEqual("", c.to_vector())
    # Calling unsed when not present should not raise.
    c.unset(AV.network)

  def test_set_invalid(self):
    c = Cvss()
    self.assertRaises(ValueError, c.set, "not valid")

  def test_repr(self):
    c = Cvss()
    self.assertTrue(str(c))

  def test_set_removes_existing(self):
    c = Cvss()
    c.set(AV.network)
    self.assertEqual("AV:N", c.to_vector())
    c.set(AV.local)
    self.assertEqual("AV:L", c.to_vector())

  def test_has(self):
    c = Cvss()
    c.set(AV.network)
    self.assertTrue(c.has(AV.network))
    self.assertFalse(c.has(AV.local))


if __name__ == "__main__":
  unittest.main()
