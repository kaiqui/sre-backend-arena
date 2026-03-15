FROM gradle:8.5-jdk17 AS builder

WORKDIR /app
COPY build.gradle.kts settings.gradle.kts ./
COPY src ./src
RUN gradle shadowJar --no-daemon

FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Datadog APM agent
ADD https://dtdg.co/latest-java-tracer /app/dd-java-agent.jar

COPY --from=builder /app/build/libs/*-all.jar app.jar

RUN chown -R appuser:appgroup /app
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget -q --spider http://localhost:8080/health/live || exit 1

EXPOSE 8080

ENV JAVA_OPTS="-Xms64m -Xmx200m -XX:+UseG1GC -XX:+HeapDumpOnOutOfMemoryError"

CMD ["sh", "-c", "java $JAVA_OPTS -javaagent:/app/dd-java-agent.jar -Ddd.profiling.enabled=true -jar /app/app.jar"]
