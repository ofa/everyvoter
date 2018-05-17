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


// Files that should be copied over as-is
const vendorStylePaths = {
    src: [],
    dest: `${dirs.dest}/css/vendor`
}
const vendorJSPaths = {
    src: [
        'node_modules/bootstrap/dist/js/bootstrap.js',
    ],
    dest: `${dirs.dest}/js/vendor`
}
const imgPaths = {
    src: [
        `${dirs.src}/img/**`,
    ],
    dest: `${dirs.dest}/img`
}
const fontPaths = {
    src: [
        `${dirs.src}/fonts/**`,
    ],
    dest: `${dirs.dest}/fonts`
}


// Paths related to CodeMirror (these can be concatinated)
const codeMirrorPaths = {
    src: [
        'node_modules/codemirror/lib/codemirror.js',
        'node_modules/codemirror/addon/mode/overlay.js',
        'node_modules/codemirror/mode/django/django.js',
        'node_modules/codemirror/mode/htmlmixed/htmlmixed.js',
        'node_modules/codemirror/mode/xml/xml.js',
        'node_modules/codemirror/mode/css/css.js'
        ],
    dest: `${dirs.dest}/js/vendor`
}


// Paths related to app management/admin
const managePaths = {
    scssSource: `${dirs.src}/scss/manage/*.scss`,
    scssWatch: `${dirs.src}/scss/manage/**/**.scss`,
    scssDest: `${dirs.dest}/css/manage`,
    jsSource: [
        `${dirs.src}/js/manage/manage_core.js`,
        `${dirs.src}/js/manage/pages/*.js`
    ],
    jsWatch: [
        `${dirs.src}/manage/js/core.js`,
        `${dirs.src}/manage/js/pages/*.js`
    ],
    jsDest: `${dirs.dest}/js/manage`
}

// Paths related to end-user constituents webpages
const constituentPaths = {
    scssSource: `${dirs.src}/scss/constituent/*.scss`,
    scssWatch: `${dirs.src}/scss/constituent/**/**.scss`,
    scssDest: `${dirs.dest}/css/constituent`,
    jsSource: [
        `${dirs.src}/js/constituent/constituent_core.js`,
        `${dirs.src}/js/constituent/pages/*.js`
    ],
    jsWatch: [
        `${dirs.src}/constituent/js/core.js`,
        `${dirs.src}/constituent/js/pages/*.js`
    ],
    jsDest: `${dirs.dest}/js/constituent`
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

/* Simple task to copy files from their source dir to the dest */
gulp.task('simple_copy', () => {
    gulp.src(vendorStylePaths.src)
        .pipe(gulp.dest(vendorStylePaths.dest));
    gulp.src(vendorJSPaths.src)
        .pipe(gulp.dest(vendorJSPaths.dest));
    gulp.src(imgPaths.src)
        .pipe(gulp.dest(imgPaths.dest));
    gulp.src(fontPaths.src)
        .pipe(gulp.dest(fontPaths.dest));
});

/* Simple codemirror task */
gulp.task('codemirrorconcat', () => {
    gulp.src(codeMirrorPaths.src)
        .pipe(uglify())
        .pipe(concat('codemirror-combined.js'))
        .pipe(gulp.dest(codeMirrorPaths.dest));
});

/* Constituent Tasks */
gulp.task('constituent_scss', () => {
    gulp.src(constituentPaths.scssSource)
        .pipe(sourcemaps.init({largeFile: true}))
        .pipe(sass().on('error', error))
        .pipe(autoprefixer({browsers: ['last 2 versions']}))
        .pipe(sourcemaps.write('maps/'))
        .pipe(gulp.dest(constituentPaths.scssDest))
        .pipe(livereload())
        .pipe(notify({ message: 'Constituent styles task complete' }));
});

gulp.task('constituent_js', () => {
    gulp.src(constituentPaths.jsSource)
        .pipe(concat('constituent.js'))
        .pipe(babel().on('error', error))
        .pipe(gulp.dest(constituentPaths.jsDest))
        .pipe(livereload())
        .pipe(notify({ message: 'Constituent scripts task complete' }));
});


/* Manage/Admin Tasks */
gulp.task('manage_scss', () => {
    gulp.src(managePaths.scssSource)
        .pipe(sourcemaps.init({largeFile: true}))
        .pipe(sass().on('error', error))
        .pipe(autoprefixer({browsers: ['last 2 versions']}))
        .pipe(sourcemaps.write('maps/'))
        .pipe(gulp.dest(managePaths.scssDest))
        .pipe(livereload())
        .pipe(notify({ message: 'Manage styles task complete' }));
});

gulp.task('manage_js', () => {
    gulp.src(managePaths.jsSource)
        .pipe(concat('manage.js'))
        .pipe(babel().on('error', error))
        .pipe(gulp.dest(managePaths.jsDest))
        .pipe(livereload())
        .pipe(notify({ message: 'Manage scripts task complete' }));
});


gulp.task('watch', () => {
    livereload.listen();

    gulp.watch(constituentPaths.scssWatch, ['constituent_scss']);
    gulp.watch(constituentPaths.jsWatch, ['constituent_js']);
    gulp.watch(managePaths.scssWatch, ['manage_scss']);
    gulp.watch(managePaths.jsWatch, ['manage_js']);
});

/* Default task to process all */
gulp.task('default', [
    'simple_copy',
    'codemirrorconcat',
    'constituent_scss',
    'constituent_js',
    'manage_scss',
    'manage_js'
]);

/* Develop */
gulp.task('develop', [
    'default',
    'watch'
]);
