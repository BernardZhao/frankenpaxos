package frankenpaxos.multipaxos

import frankenpaxos.simulator._
import org.scalatest.FlatSpec

class MultiPaxosTest extends FlatSpec {
  "A Paxos instance" should "only ever choose a single value" in {
    // TODO(mwhittaker): Uncomment. This test is currently failing.
    // // TODO(mwhittaker): If a test case fails, show the log.
    // // TODO(mwhittaker): Uniquely id each message.
    // for (f <- 1 to 3) {
    //   val sim = new SimulatedMultiPaxos(f)
    //   Simulator
    //     .simulate(sim, runLength = 100, numRuns = 1000)
    //     .flatMap(b => Simulator.minimize(sim, b.history)) match {
    //     case Some(BadHistory(history, error)) => {
    //       val formatted_history = history.map(_.toString).mkString("\n")
    //       fail(s"Error: $error\n$formatted_history")
    //     }
    //     case None => {}
    //   }
    // }
  }
}
