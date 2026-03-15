import tracer from 'dd-trace';

tracer.init({
  service: process.env.DD_SERVICE || 'pokemon-battle-api',
  env: process.env.DD_ENV || 'production',
  version: process.env.DD_VERSION || '1.0.0',
  logInjection: true,
});

export default tracer;
