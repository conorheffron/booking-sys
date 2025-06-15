module.exports = {
  preset: 'ts-jest',
  setupFilesAfterEnv: ['<rootDir>/setupTests.ts'],
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
  },
  // Mock CSS and static files:
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|webp|svg)$': '<rootDir>/src/components/__mocks__/fileMock.js',
  },
  // Optional: transformIgnorePatterns to ignore some modules if needed
  // transformIgnorePatterns: [
  //   "node_modules/(?!MODULE_TO_TRANSPILE)"
  // ],
};
