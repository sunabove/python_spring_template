import aspose.slides as slides

from IPython.display import clear_output

clear_output()

# Load the presentation file
ppt = slides.Presentation( "c:/test/test.pptx" )

# Create HTML options
options = slides.export.HtmlOptions()
# Create a responsive HTML controller
controller = slides.export.ResponsiveHtmlController() 
# Set controller as HTML formatter
options.html_formatter = slides.export.HtmlFormatter.create_custom_formatter(controller)

# 각 슬라이드를 개별 HTML 파일로 변환합니다.
for i, slide in enumerate( ppt.slides ):
    # 새로운 프레젠테이션 객체를 생성합니다.
    single_slide_presentation = slides.Presentation()
    # 모든 슬라이드를 제거합니다.
    single_slide_presentation.slides.remove_at(0)
    # 현재 슬라이드를 추가합니다.
    single_slide_presentation.slides.insert_clone(0, slide) 
    
    # 슬라이드를 HTML로 저장합니다.
    file_path = f"c:/test/test_{i+1:03d}.html"
    
    print( f"saving a ppt slide to {file_path} ..." )    
    single_slide_presentation.save(file_path, slides.export.SaveFormat.HTML, options )

    content = ""
    
    # convert utf-8-bom to utf-8
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        # 파일의 모든 내용을 읽어들입니다.
        content = file.read().strip()
    pass

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write( content )
    pass
    # // convert utf-8-bom to utf-8

    #continue 

    with open(file_path, 'r', encoding='utf-8') as file:
        # 파일의 모든 내용을 읽어들입니다.
        content = file.read().strip()
    pass

    with open(file_path, 'w', encoding='utf-8') as file:

        if 1 : 
            # remove water-mark
            idxApose = content.index( "Created with Aspose.Slides" )
            idxGtransform = content.rfind( "<g transform=\"matrix", 0, idxApose )

            idxPtyLtd = content.rindex( "Aspose Pty Ltd.", idxApose )
            idxG = content.index( "</g>", idxPtyLtd )

            a = content[ 0 : idxGtransform ]
            b = content[ idxG + 4 : ]
            content = a + b
            # // remove water-mark
        pass

        if 1 : 
            # remove slide title
            idxSlideTtitleStart = content.index( "<div class=\"slideTitle\">" )
            idxSlideTtitleClose = content.index( "</div>", idxSlideTtitleStart )

            a = content[ 0 : idxSlideTtitleStart ]
            b = content[ idxSlideTtitleClose + 5 : ]
            content = a + b
            # // remove slide title
        pass

        file.write( content )
    pass
pass

print( f"Converted {len(ppt.slides)} slides to HTML files." )

# Save as HTML
#all_html_file = "c:/test/test.html"
#ppt.save( "c:/test/test.html", slides.export.SaveFormat.HTML, options)

