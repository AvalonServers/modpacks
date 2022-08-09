#!/usr/bin/env bash
java -jar server.jar -Xms4G -Xmx8G -Dio.netty.leakDetection.level=advanced
