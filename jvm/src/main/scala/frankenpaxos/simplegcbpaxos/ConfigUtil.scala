package frankenpaxos.simplegcbpaxos

import frankenpaxos.NettyTcpAddress
import frankenpaxos.NettyTcpTransport
import java.net.InetSocketAddress

object ConfigUtil {
  def fromProto(proto: NettyConfigProto): Config[NettyTcpTransport] = {
    def addr(hostPort: HostPortProto): NettyTcpAddress =
      NettyTcpAddress(new InetSocketAddress(hostPort.host, hostPort.port))

    Config(
      f = proto.f,
      leaderAddresses = proto.leaderAddress.map(addr),
      proposerAddresses = proto.proposerAddress.map(addr),
      depServiceNodeAddresses = proto.depServiceNodeAddress.map(addr),
      acceptorAddresses = proto.acceptorAddress.map(addr),
      replicaAddresses = proto.replicaAddress.map(addr),
      garbageCollectorAddresses = proto.garbageCollectorAddress.map(addr)
    )
  }

  def fromFile(filename: String): Config[NettyTcpTransport] = {
    val source = scala.io.Source.fromFile(filename)
    try {
      fromProto(NettyConfigProto.fromAscii(source.mkString))
    } finally {
      source.close()
    }
  }
}
