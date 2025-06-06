url = [
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/4/6/4669a54192333054802_01.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/8/9/895a8e0CLINI00000002_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/8/b/8ba4f44887167485495_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/4/f/4fe19a2773602042951-01.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/5/6/562de4e20714851125_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/7/0/70ea50bMACXX00001499_01.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/a/b/abeb16c651986702480.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/8/b/8ba4f44773602345830_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/6/c/6c94af118084977347_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/9/f/9fa28c5MACXX00001523_a3.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/3/d/3d1429a773602376124_rv__1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/4/f/4fe19a2773602422029_01.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/a/8/a8bf4c2AVEDA00000097_0.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/5/6/562de4e20714215552_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/d/1/d123951716170027456_3.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/a/3/a3c482527131043317_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/e/5/e5d803eAVEDA00000838_01.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/4/b/4bb8800607710004733_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/b/8/b861cddESTEE00000133_1.jpg",
    "https://images-static.nykaa.com/media/catalog/product/tr:w-220,h-220,cm-pad_resize/d/1/d1db285607710089631_1.jpg",
]

# import pandas as pd

# df = pd.DataFrame(url,columns=["URL"])
# df.to_csv("nykaa_images.csv", index=False)

# print(df)


urls_string = ",".join(url)

# Save the string to a CSV file
with open("nykaa_images.csv", "w") as file:
    file.write(urls_string)

print("URLs have been written to nykaa_images.csv")
