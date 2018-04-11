'use strict';

import gulp from 'gulp';
import autoprefixer from 'gulp-autoprefixer';
import babel from 'gulp-babel';
import browserify from 'gulp-browserify';
import cleanCss from 'gulp-clean-css';
import concat from 'gulp-concat';
import jshint from 'gulp-jshint';
import livereload from 'gulp-livereload';
import notify from 'gulp-notify';
import rename from 'gulp-rename';
import sass from 'gulp-sass';
import sourcemaps from 'gulp-sourcemaps';
import uglify from 'gulp-uglify';
import gutil from 'gulp-util';

/* Set variables for the different paths */
const dirs = {
    src: 'assets',
    dest: 'dist'
};

const scssPaths = {
    src: `${dirs.src}/scss/*.scss`,
    watch: `${dirs.src}/scss/**/**.scss`,
    dest: `${dirs.dest}/css`,
    destMin: `${dirs.dest}/css-min`
};

const vendorConcatPaths = {
    src: [
            'node_modules/js-cookie/src/js.cookie.js',
            'node_modules/popper.js/dist/umd/popper.js',
            'node_modules/bootstrap/dist/js/bootstrap.js',
        ],
    dest: `${dirs.dest}/js-min`
}

const vendorOtherPaths = {
    src: [],
    dest: `${dirs.dest}/js-min/vendor`
}

const jsPaths = {
    src: [
            `${dirs.src}/js/core.js`,
            `${dirs.src}/js/pages/*.js`
        ],
    watch: `${dirs.src}/js/**`,
    dest: `${dirs.dest}/js`,
    destMin: `${dirs.dest}/js-min`
};

const imgPaths = {
    src: `${dirs.src}/img/**`,
    dest: `${dirs.dest}/img`
};

const fontsPaths = {
    src: `${dirs.src}/fonts/**`,
    dest: `${dirs.dest}/fonts/`
}

/* Function to process errors and present them in a nice visual manner */
function error(err) {
    /* Human readable message for notification and console */
    var message = `Error ocurred on line ${err.line} in ${err.relativePath}`;

    /* Send notification */
    notify().write(message);

    /* Log message and error in Gulp console */
    gutil.log(gutil.colors.bgRed.black(message));
    gutil.log(err.toString());

    /* Emit end to allow watch to continue */
    this.emit('end');
}

/* Task processes SCSS, autoprefixes, and creates
   standard and min stylesheets */
gulp.task('scss', () => {
    gulp.src(scssPaths.src)
        .pipe(sourcemaps.init({largeFile: true}))
        .pipe(sass().on('error', error))
        .pipe(autoprefixer({browsers: ['last 2 versions']}))
        .pipe(sourcemaps.write('maps/'))
        .pipe(gulp.dest(scssPaths.dest))
        .pipe(cleanCss())
        .pipe(gulp.dest(scssPaths.destMin))
        .pipe(livereload())
        .pipe(notify({ message: 'Styles task complete' }));
});

gulp.task('vendorConcat', () => {
    gulp.src(vendorConcatPaths.src)
        .pipe(concat('vendor.js'))
        .pipe(gulp.dest(vendorConcatPaths.dest));
});

gulp.task('vendorOther', () =>{
    gulp.src(vendorOtherPaths.src)
        .pipe(uglify())
        .pipe(gulp.dest(vendorOtherPaths.dest));
});


/* Task processes JavaScript through Babel and browserify
   creates standard and uglified versions */
/* Initial setup was supposed to rely on Babel and browserify,
   but due to resource constraints, we are switching to a simplified solution.
gulp.task('js', () => {
    gulp.src(jsPaths.src)
        .pipe(babel().on('error', error))
        .pipe(browserify({extensions: ['.js']}))
        .pipe(gulp.dest(jsPaths.dest))
        .pipe(uglify())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(jsPaths.destMin))
        .pipe(livereload())
        .pipe(notify({ message: 'Scripts task complete' }));
});

*/
gulp.task('js', () => {
    gulp.src(jsPaths.src)
        .pipe(concat('everyvoter.js'))
        .pipe(babel().on('error', error))
        .pipe(gulp.dest(jsPaths.dest))
        .pipe(uglify())
        .pipe(gulp.dest(jsPaths.destMin))
        .pipe(livereload())
        .pipe(notify({ message: 'Scripts task complete' }));
});

/* Simple task to move img assets to the dist folder */
gulp.task('img', () =>{
    gulp.src(imgPaths.src)
        .pipe(gulp.dest(imgPaths.dest));
});

/* Task to move fonts to the dist folder */
gulp.task('fonts', () =>{
    gulp.src(fontsPaths.src)
        .pipe(gulp.dest(fontsPaths.dest));
});


/* Watch function with live reload */
gulp.task('watch', () => {
    livereload.listen();

    gulp.watch(scssPaths.watch, ['scss']);
    gulp.watch(jsPaths.watch, ['js']);
    gulp.watch(imgPaths.src, ['img']);
});

/* Default task to process all and start watch */
gulp.task('default', ['scss','vendorConcat','vendorOther','js','img','fonts','watch']);

/* Build task to run during build processes */
gulp.task('build', ['scss','vendorConcat','vendorOther','js','img','fonts']);

/* Develop */
gulp.task('develop', ['build','watch']);
