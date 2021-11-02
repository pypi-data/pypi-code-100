from heliosphere import initialize, HeliosphereConfig, HeliosphereTags


config = HeliosphereConfig(
    api_token='dummy_token',
    service_name='dummy_service',
    collector_endpoint='http://localhost:4317',
    sampling_ratio=1
)

hs = initialize(config)


tracer = hs.get_tracer_provider().get_tracer('heliosphere.sdk.test')

with tracer.start_as_current_span('test-span',
                                  attributes={
                                      HeliosphereTags.TEST_TRIGGERED_TRACE: HeliosphereTags.TEST_TRIGGERED_TRACE}
                                  ) as span:
    if not span.is_recording or not span.get_span_context().trace_flags.sampled:

        print('Span is not recording. exiting...')
        exit(1)
    span.add_event("test event!")

hs.uninstrument()
