module.exports = {
    preset: '@vue/cli-plugin-unit-jest',
    verbose: true,
    moduleFileExtensions: [
        'js',
        'json',
        'vue'
    ],
    collectCoverage: true,
    coverageDirectory: './tests/coverage',
    collectCoverageFrom: ['./src/**/*.{js,vue}'],
    coverageProvider: 'v8',
    coverageReporters: ['text', 'html', 'cobertura']
}
