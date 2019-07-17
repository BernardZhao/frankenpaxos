package frankenpaxos.epaxos

import frankenpaxos.NettyTcpAddress
import frankenpaxos.NettyTcpTransport
import java.net.InetSocketAddress

object ConfigUtil {
  def fromProto(proto: NettyConfigProto): Config[NettyTcpTransport] = {
    Config(f = proto.f,
           leaderAddresses = proto.leaderAddress.map(
             hp => NettyTcpAddress(new InetSocketAddress(hp.host, hp.port))
           ))
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
