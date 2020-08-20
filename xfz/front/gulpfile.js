var gulp = require('gulp');
var cssnano = require('gulp-cssnano');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var cache = require('gulp-cache');
var imagemin = require('gulp-imagemin');
var bs = require('browser-sync').create();
var scss = require('gulp-sass');
var util = require('gulp-util');
var sourcemaps = require('gulp-sourcemaps');
var terser = require('gulp-terser');


var path = {
    'css':'./src/css/**/',
    'js':'./src/js/',
    'images':'./src/images/',
    'html':'./templates/**/',
    'csspath':'./dist/css/',
    'jspath':'./dist/js/',
    'imagespath':'./dist/images/'
};


gulp.task('css',function (done) {
    gulp.src(path.css + '*.scss')
        .pipe(scss().on('error',scss.logError))
        .pipe(cssnano())
        .pipe(rename({'suffix':'.min'}))
        .pipe(gulp.dest(path.csspath))
        .pipe(bs.stream());
    done();
});

gulp.task('js',function (done) {
    gulp.src(path.js + '*.js')
        .pipe(sourcemaps.init())
        .pipe(terser().on('error',util.log))
        .pipe(rename({'suffix':'.min'}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.jspath))
        .pipe(bs.stream());
    done();
});

gulp.task('images',function (done) {
    gulp.src(path.images + '*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.imagespath))
        .pipe(bs.stream());
    done();
});

gulp.task('html',function (done) {
    gulp.src(path.html + '*.html')
        .pipe(bs.stream());
    done();
});

gulp.task('bs',function (done) {
    bs.init({
        'server':{
            'baseDir':'./'
        }
    });
    done();
});

gulp.task('watch',function (done) {
    gulp.watch(path.css + '*.scss',gulp.series('css'));
    gulp.watch(path.js + '*.js',gulp.series('js'));
    gulp.watch(path.images + '*.*',gulp.series('images'));
    gulp.watch(path.html + '*.html',gulp.series('html'));
    done();
});

// gulp.task('default',gulp.parallel('bs','watch'));
gulp.task('default', gulp.series('watch'));




