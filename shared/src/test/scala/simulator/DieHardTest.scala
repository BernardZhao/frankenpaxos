package frankenpaxos.simulator

import org.scalatest._

class DieHardSpec extends FlatSpec {
  "Die Hard jugs" should "always satisfy their type invariants" in {
    val sim = new SimulatedDieHard()
    Simulator
      .simulate(sim, runLength = 10, numRuns = 100)
      .flatMap(b => Simulator.minimize(sim, b.history)) match {
      case Some(BadHistory(history, error)) =>
        fail(s"Error: $error\n$history")
      case None => {}
    }
  }
}
