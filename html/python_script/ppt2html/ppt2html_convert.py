import aspose.slides as slides
import argparse
import os
from pathlib import Path

file_path = "/home/user/documents/example.txt"

def convert_ppt_to_html(ppt_file_path):
    print(f"Converting ppt file to html : {ppt_file_path} ...")

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
    html_file_name_prev = Path( ppt_file_path ).name.split( "." )[0]

    # 각 슬라이드를 개별 HTML 파일로 변환합니다.
    for i, slide in enumerate( ppt.slides ):
        # 새로운 프레젠테이션 객체를 생성합니다.
        single_slide_presentation = slides.Presentation()
        # 모든 슬라이드를 제거합니다.
        single_slide_presentation.slides.remove_at(0)
        # 현재 슬라이드를 추가합니다.
        single_slide_presentation.slides.insert_clone(0, slide) 
        
        # 슬라이드를 HTML로 저장합니다.
        html_file_path = str(folder_path / f"{i+1:04d}.html")
        
        print( f"saving a ppt slide to {html_file_path} ..." )    
        single_slide_presentation.save( html_file_path, slides.export.SaveFormat.HTML, options )

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

            if "Created with Aspose.Slides" in content:
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
                # 슬라이드 제목 제거
                slide_title_tag = "<div class=\"slideTitle\">"
                slide_title_end_tag = "</div>"
                
                idxSlideTitleStart = content.find(slide_title_tag)
                if idxSlideTitleStart > -1:
                    idxSlideTitleClose = content.find(slide_title_end_tag, idxSlideTitleStart)
                    if idxSlideTitleClose > -1:
                        a = content[0:idxSlideTitleStart]
                        b = content[idxSlideTitleClose + len(slide_title_end_tag):]
                        content = a + b
                    pass
                pass
            pass

            if True :
                # 1. viewBox 수정
                content = content.replace('viewBox="0 0 720 540"', 'viewBox="0 0 960 540"')

                # 2. <image> 태그의 width와 height 수정
                content = content.replace('width="720"', 'width="960"')
                content = content.replace('height="540"', 'height="540"')

                # 2. CSS 수정
                new_css = """
                .slides-canvas {
                    display: block;
                    margin: 0 auto;
                    width: 100%;
                    height: auto;
                    aspect-ratio: 16 / 9;
                }
                """
                content = content.replace( '<style>.slide {', '<style>' + new_css + '}\n.slide {' )
            pass

            file.write( content )
        pass
    pass

    print( f"Converted {len(ppt.slides)} slides to HTML files." )
pass # convert_slide_to_html

def check_and_convert_ppts_in_folder(folder_path):
    # Recursively search for .pptx files
    for ppt_file in Path(folder_path).rglob("*.pptx"):
        ppt = slides.Presentation(ppt_file)

        # Get the modification time of the PPT file
        ppt_mod_time = ppt_file.stat().st_mtime

        # Get the list of all HTML files for the corresponding PPT file
        html_files = [str(ppt_file.parent / f"{i+1:04d}.html") for i in range(len(ppt.slides))]

        # Get the modification times of all the HTML files
        html_files_mtime = {html_file: os.path.getmtime(html_file) for html_file in html_files if os.path.exists(html_file)}

        # Check if the PPT file's modification time is newer than all HTML files
        ppt_needs_conversion = False
        for html_file in html_files:
            html_mod_time = html_files_mtime.get(html_file, 0)  # If HTML doesn't exist, consider it as 0
            if ppt_mod_time > html_mod_time:
                ppt_needs_conversion = True
                break

        if ppt_needs_conversion:
            print(f"PPT file {ppt_file} is newer than corresponding HTML files. Converting all slides...")
            # Convert all slides to HTML
            for i in range(len(ppt.slides)):
                convert_ppt_to_html( ppt_file )
        else:
            print(f"Skipping PPT file {ppt_file}, as all HTML files are up-to-date.")
        pass
    pass
pass # check_and_convert_ppts_in_folder

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder path to search for ppt files")
    args = parser.parse_args()

    check_and_convert_ppts_in_folder(args.folder)
pass