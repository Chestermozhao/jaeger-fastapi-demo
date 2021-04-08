from fastapi import FastAPI
from starlette.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor


def get_application() -> FastAPI:

    trace.set_tracer_provider(TracerProvider())
    jaeger_exporter = JaegerSpanExporter(
        service_name="Jaeger Demo App", agent_host_name="jaeger-agent", agent_port=6831
        #service_name="Jaeger Demo App", collector_endpoint="http://localhost:31298/api/traces"
    )
    trace.get_tracer_provider().add_span_processor(
        BatchExportSpanProcessor(jaeger_exporter, max_export_batch_size=10)
    )

    application = FastAPI(
        title="Jaeger Demo App",
        description="Jaeger Demo App Entrypoiny",
        openapi_url="/openapi.json",
        docs_url="/docs"
    )

    # Add your routers
    FastAPIInstrumentor.instrument_app(application)
    return application


app = get_application()


@app.get("/hello")
async def hello():
    tracer = trace.get_tracer("HelloWorld")
    with tracer.start_as_current_span("HelloWroldSpan"):
        return {"message": "hello world"}
