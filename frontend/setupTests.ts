import 'whatwg-fetch';
import '@testing-library/jest-dom';

if (typeof global.TextEncoder === 'undefined') {
  // @ts-ignore
  global.TextEncoder = require('util').TextEncoder;
}
if (typeof global.TextDecoder === 'undefined') {
  // @ts-ignore
  global.TextDecoder = require('util').TextDecoder;
}

// Optional: Mock static file imports if not handled by your test environment
// jest.mock('src/img/robot-logo.png', () => 'robot-logo.png');
