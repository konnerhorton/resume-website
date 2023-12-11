require("dotenv").config();

module.exports = {
    // Website title, shown in left sidebar and in page title
    title: "Konner Horton",
    // Site URL to generate absolute URLs. Used across the board.
    url: process.env.URL || "http://konnerhorton.com",
    // Profile image for left sidebar
    image: "/assets/images/image_original.jpg",
    // Image alt text for left sidebar
    imageAlt: "Konner Horton",
    // Author name, shown in left sidebar, and used in JSON-LD
    author: "Konner Horton",
    // Site description, shown below site image (optional)
    description: "konnerhorton@gmail.com",
    // OpenGraph default image, in case you don't have an `image`
    // set in your Markdown frontmatter; relevant for social
    // sharing.
    openGraphDefaultImage: "/assets/images/opengraph.jpg",
    // GitHub ID (optional, remove it not needed), used for link in the left sidebar
    socialGitHub: "konnerhorton",
    
};
