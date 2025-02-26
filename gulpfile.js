var gulp = require('gulp');
var sass = require('gulp-sass')(require('sass'));
var prefix = require('gulp-autoprefixer');
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var cache = require('gulp-cache');
var cp = require('child_process');
var browserSync = require('browser-sync').create();

var jekyll = process.platform === 'win32' ? 'jekyll.bat' : 'jekyll';

// Compile SASS
function compileSass() {
    return gulp.src('assets/css/scss/main.scss')
        .pipe(sass({
            outputStyle: 'expanded',
            onError: browserSync.notify
        }))
        .pipe(prefix(['last 15 versions', '> 1%', 'ie 8', 'ie 7'], { cascade: true }))
        .pipe(gulp.dest('_site/assets/css'))
        .pipe(browserSync.stream())
        .pipe(gulp.dest('assets/css'));
}

// Compress Images
function compressImages() {
    return gulp.src('assets/img/**/*')
        .pipe(cache(imagemin({
            interlaced: true,
            progressive: true,
            svgoPlugins: [{ removeViewBox: false }],
            use: [pngquant()]
        })))
        .pipe(gulp.dest('_site/assets/img'))
        .pipe(browserSync.stream());
}

// Build Jekyll Site
function jekyllBuild(done) {
    return cp.spawn(jekyll, ['build'], { stdio: 'inherit' })
        .on('close', done);
}

// Reload Browser
function browserReload(done) {
    browserSync.reload();
    done();
}

// Start BrowserSync
function browserSyncServe(done) {
    browserSync.init({
        server: {
            baseDir: '_site'
        },
        notify: false
    });
    done();
}

// Watch Files
function watchFiles() {
    gulp.watch('assets/css/scss/**/*.scss', compileSass);
    gulp.watch('assets/js/**/*.js', gulp.series(jekyllBuild, browserReload));
    gulp.watch('assets/img/**/*', compressImages);
    gulp.watch(
        ['*.html', '_layouts/*.html', '_includes/*.html', '_pages/*.html', '_posts/*'],
        gulp.series(jekyllBuild, browserReload)
    );
}

// Define Complex Tasks
const build = gulp.series(compileSass, compressImages, jekyllBuild);
const serve = gulp.series(build, browserSyncServe);
const watch = gulp.parallel(watchFiles, serve);

// Export Tasks
exports.sass = compileSass;
exports.images = compressImages;
exports.jekyll = jekyllBuild;
exports.build = build;
exports.serve = serve;
exports.default = watch;