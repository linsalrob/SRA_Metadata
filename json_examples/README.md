# JSON Examples

These are some example data from the August 2019 SRA metadata that were chosen at random. Quite literally! 

I used this command:

```bash
ls json | sort -R | head | xargs -i cp json/{} json_examples
```

(`sort -R` is a good command to have up your sleeves).

These ten files represent a random selection of metadata, and hopefully will have some of the variation we see in the whole directory (but probably not all of it). They are good to use with the code in [the json directory](../json) to see what the contents of typical json files are.