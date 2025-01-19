To include a video in a Markdown (.md) file, you generally use an HTML `<video>` tag as Markdown itself doesn't natively support video embedding. Here's a simple example:

```markdown
<video width="320" height="240" controls>
  <source src="movie.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

This will embed a video into your Markdown document, assuming the video file is located in the same directory or the specified path.