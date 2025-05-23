const { format, formatISO, getYear } = require("date-fns");
const pluginRss = require("@11ty/eleventy-plugin-rss");
const pluginToc = require("eleventy-plugin-toc");
const { MD5 } = require("crypto-js");
const { URL } = require("url");
const { readFileSync } = require("fs");
const fs = require('fs');
const path = require('path');
const siteconfig = require("./content/_data/siteconfig.js");
const markdownIt = require("markdown-it");
const markdownItReplaceLink = require("markdown-it-replace-link");
const markdownItAnchor = require("markdown-it-anchor");
const syntaxHighlight = require("@11ty/eleventy-plugin-syntaxhighlight");
const mathjaxPlugin = require("eleventy-plugin-mathjax");


module.exports = function (eleventyConfig) {
    // Set Markdown library
    eleventyConfig.setLibrary(
        "md",
        markdownIt({
            html: true,
            xhtmlOut: true,
            linkify: true,
            typographer: true,
        }).use(markdownItAnchor).use(markdownItReplaceLink, {replaceLink: function(link) {return link.replace(/\.md(#[^#]+)?$/, "$1")}})
    );
    // Plugin for syntaxHighlight
    eleventyConfig.addPlugin(syntaxHighlight);

    // Define an asynchronous Nunjucks shortcode for Plotly charts
    eleventyConfig.addAsyncShortcode("plotlyChart", async function (chartId, filePath) {
        const chartFilePath = path.join(__dirname, 'content/posts/plotly', filePath);
        try {
            const chartJson = await fs.promises.readFile(chartFilePath, 'utf-8');
            return `<div id="${chartId}" class="plotly-chart-container" style="all: initial;">
            <script>
            const chartData = JSON.parse(\`${chartJson}\`);
            Plotly.newPlot("${chartId}", chartData.data, chartData.layout);
            </script>
        </div>`;
        } catch (error) {
            console.error('Error reading chart JSON file:', error);
            return `<p>Error loading chart.</p>`;
        }
    });

    // Add functionality for MathJax
    eleventyConfig.addPlugin(mathjaxPlugin, {
        output: "chtml",
        chtml: {
          fontURL:
            "https://cdn.jsdelivr.net/npm/mathjax@3/es5/output/chtml/fonts/woff-v2",
        },
      });
    
    // Define passthrough for assets
    eleventyConfig.addPassthroughCopy("assets");

    // Add watch target for JS files (needed for JS bundling in dev mode)
    eleventyConfig.addWatchTarget("./assets/js/");
    // And to make this work we've to disable the .gitignore usage of eleventy.
    eleventyConfig.setUseGitIgnore(false);

    // Add 3rd party plugins
    eleventyConfig.addPlugin(pluginRss);
    eleventyConfig.addPlugin(pluginToc);

    // Define 11ty template formats
    eleventyConfig.setTemplateFormats([
        "njk",
        "md",
        "svg",
        "jpg",
        "css",
        "png"
    ]);

    // Generate excerpt from first paragraph
    eleventyConfig.addShortcode("excerpt", (article) =>
        extractExcerpt(article)
    );

    // Set absolute url
    eleventyConfig.addNunjucksFilter("absoluteUrl", (path) => {
        return new URL(path, siteconfig.url).toString();
    });


    // Returns CSS class for home page link
    eleventyConfig.addNunjucksFilter("isHomeLink", function (url, pattern) {
        return pattern === "/" && url === "/" ? "active" : "";
    });

    // Returns CSS class for active page link
    eleventyConfig.addNunjucksFilter("isActiveLink", function (url, pattern) {
        return url.length > 1 && url.startsWith(pattern) ? "active" : "";
    });

    // Format dates for sitemap
    eleventyConfig.addNunjucksFilter("sitemapdate", function (date) {
        return format(date, "yyyy-MM-dd");
    });

    // Format dates for JSON-LD
    eleventyConfig.addNunjucksFilter("isodate", function (date) {
        return formatISO(date);
    });

    // Extracts the year from a post
    eleventyConfig.addNunjucksFilter("year", function (post) {
        if (post && post.date) {
            return getYear(post.date);
        }
        return "n/a";
    });

    // Extracts the day of a date
    eleventyConfig.addNunjucksFilter("day", function (date) {
        return format(date, "dd");
    });

    // Extracts the month of a date
    eleventyConfig.addNunjucksFilter("month", function (date) {
        return format(date, "MMM");
    });

    // Extracts readable date of a date
    eleventyConfig.addNunjucksFilter("readableDate", function (date) {
        return format(date, "yyyy-MM-dd");
    });

    // Add custom hash for cache busting
    const hashes = new Map();
    eleventyConfig.addNunjucksFilter("addHash", function (absolutePath) {
        const cached = hashes.get(absolutePath);
        if (cached) {
            return `${absolutePath}?hash=${cached}`;
        }
        const fileContent = readFileSync(`${process.cwd()}${absolutePath}`, {
            encoding: "utf-8"
        }).toString();
        const hash = MD5(fileContent.toString());
        hashes.set(absolutePath, hash);
        return `${absolutePath}?hash=${hash}`;
    });

    // Create custom collection for getting the newest 5 updates
    eleventyConfig.addCollection("recents", function (collectionApi) {
        return collectionApi.getAllSorted().reverse().slice(0, 5);
    });

    // Plugin for setting _blank and rel=noopener on external links in markdown content
    eleventyConfig.addPlugin(require("./_11ty/external-links.js"));

    // Plugin for transforming images
    eleventyConfig.addPlugin(require("./_11ty/srcset.js"));

    // Plugin for minifying HTML
    eleventyConfig.addPlugin(require("./_11ty/html-minify.js"));

    return {
        dir: {
            // Consolidating everything below the `content` folder
            input: "content"
        }
    };
};

// Taken from here => https://keepinguptodate.com/pages/2019/06/creating-blog-with-eleventy/
function extractExcerpt(article) {
    if (!Object.prototype.hasOwnProperty.call(article, "templateContent")) {
        console.warn(
            'Failed to extract excerpt: Document has no property "templateContent".'
        );
        return null;
    }

    const content = article.templateContent;

    const excerpt = content.slice(0, content.indexOf("\n"));

    return excerpt;
}
