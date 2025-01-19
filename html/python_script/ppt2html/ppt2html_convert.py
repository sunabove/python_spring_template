import aspose.slides as slides
import argparse
from pathlib import Path

file_path = "/home/user/documents/example.txt"

def convert_ppt_to_html( ) : 
    parser = argparse.ArgumentParser()
    parser.add_argument("ppt_file", help="ppt file")
    args = parser.parse_args()

    ppt_file_path = args.ppt_file

    print( f"Converting ppt file to html : {ppt_file_path} ..." )

    # Load the presentation file
    ppt = slides.Presentation( ppt_file_path )

    # Create HTML options
    options = slides.export.HtmlOptions()
    # Create a responsive HTML controller
    controller = slides.export.ResponsiveHtmlController() 
    # Set controller as HTML formatter
    options.html_formatter = slides.export.HtmlFormatter.create_custom_formatter(controller)

    folder_path = Path( ppt_file_path ).parent
    # ppt 확작자를 제외한 파일명의 앞 부분
    file_name_prev = Path( ppt_file_path ).name.split( "." )[0]

    # 각 슬라이드를 개별 HTML 파일로 변환합니다.
    for i, slide in enumerate( ppt.slides ):
        # 새로운 프레젠테이션 객체를 생성합니다.
        single_slide_presentation = slides.Presentation()
        # 모든 슬라이드를 제거합니다.
        single_slide_presentation.slides.remove_at(0)
        # 현재 슬라이드를 추가합니다.
        single_slide_presentation.slides.insert_clone(0, slide) 
        
        # 슬라이드를 HTML로 저장합니다.
        html_file_path = folder_path / f"{file_name_prev}_{i+1:03d}.html" 
        
        print( f"saving a ppt slide to {html_file_path} ..." )    
        single_slide_presentation.save(html_file_path, slides.export.SaveFormat.HTML, options )

        content = ""
        
        # convert utf-8-bom to utf-8
        with open(html_file_path, 'r', encoding='utf-8-sig') as file:
            # 파일의 모든 내용을 읽어들입니다.
            content = file.read().strip()
        pass

        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write( content )
        pass
        # // convert utf-8-bom to utf-8

        #continue 

        with open(html_file_path, 'r', encoding='utf-8') as file:
            # 파일의 모든 내용을 읽어들입니다.
            content = file.read().strip()
        pass

        with open(html_file_path, 'w', encoding='utf-8') as file:

            if True : 
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

            if True : 
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
pass

if __name__ == "__main__" :
    convert_ppt_to_html()
pass