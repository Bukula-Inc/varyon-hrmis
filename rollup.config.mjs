
import { terser } from 'rollup-plugin-terser';
import dynamicImportVars from '@rollup/plugin-dynamic-import-vars';
import cleaner from 'rollup-plugin-cleaner';
const timestamp = new Date().toISOString().replace(/[:.-]/g, '');

export default {
    input: 'static/js/main.js',
    output: {
        dir: 'static/build',
        format: 'es',
        preserveModules: false, 
        entryFileNames: 'bundle.min.js',
        // chunkFileNames: `chunk-[name]-${timestamp}-[hash].js`,
        chunkFileNames: `${timestamp}-[hash].js`,
    },
    plugins: [
        cleaner({
            targets: ['static/build/']
        }),
        dynamicImportVars(), 
        terser({
            ecma: 2020,
            compress: {
                drop_console: false,
                drop_debugger: true
            },
            output: {
                comments: false
            },
            mangle: true
        })
    ]
};




