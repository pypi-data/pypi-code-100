# kludge before a storm
mimetype = "application/vnd.oasis.opendocument.text"

styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles xmlns:css3t="http://www.w3.org/TR/css3-text/" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:ooo="http://openoffice.org/2004/office" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:ooow="http://openoffice.org/2004/writer" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:oooc="http://openoffice.org/2004/calc" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rpt="http://openoffice.org/2005/report" office:version="1.3">
  <office:font-face-decls>
    <style:font-face style:name="FreeMono" svg:font-family="FreeMono" style:font-family-generic="modern"  style:font-adornments="Normal" style:font-pitch="fixed"/>
    <style:font-face style:name="Times New Roman" svg:font-family="'Times New Roman'" style:font-adornments="Normal" style:font-family-generic="roman" style:font-pitch="variable"/>
    <style:font-face style:name="FreeSans" svg:font-family="FreeSans" style:font-adornments="Normal" style:font-family-generic="swiss" style:font-pitch="variable"/>
    <style:font-face style:name="DejaVu Sans" svg:font-family="'DejaVu Sans'" style:font-family-generic="system" style:font-pitch="variable"/>
    <style:font-face style:name="FreeSans1" svg:font-family="FreeSans" style:font-family-generic="system" style:font-pitch="variable"/>
  </office:font-face-decls>
  <office:styles>
    <style:default-style style:family="graphic">
      <style:graphic-properties svg:stroke-color="#3465a4" draw:fill-color="#729fcf" fo:wrap-option="no-wrap" draw:shadow-offset-x="0.3cm" draw:shadow-offset-y="0.3cm" draw:start-line-spacing-horizontal="0.283cm" draw:start-line-spacing-vertical="0.283cm" draw:end-line-spacing-horizontal="0.283cm" draw:end-line-spacing-vertical="0.283cm" style:flow-with-text="false"/>
      <style:paragraph-properties style:text-autospace="ideograph-alpha" style:line-break="strict" style:writing-mode="lr-tb" style:font-independent-line-spacing="false">
        <style:tab-stops/>
      </style:paragraph-properties>
      <style:text-properties style:use-window-font-color="true" style:font-name="Times New Roman" fo:font-size="12pt" fo:language="ru" fo:country="RU" style:letter-kerning="true" style:font-name-asian="DejaVu Sans" style:font-size-asian="10.5pt" style:language-asian="zh" style:country-asian="CN" style:font-name-complex="DejaVu Sans" style:font-size-complex="12pt" style:language-complex="hi" style:country-complex="IN"/>
    </style:default-style>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:orphans="2" fo:widows="2" fo:hyphenation-ladder-count="no-limit" style:text-autospace="ideograph-alpha" style:punctuation-wrap="hanging" style:line-break="strict" style:tab-stop-distance="1.251cm" style:writing-mode="page"/>
      <style:text-properties style:use-window-font-color="true" style:font-name="Times New Roman" fo:font-size="12pt" fo:language="ru" fo:country="RU" style:letter-kerning="true" style:font-name-asian="DejaVu Sans" style:font-size-asian="10.5pt" style:language-asian="zh" style:country-asian="CN" style:font-name-complex="DejaVu Sans" style:font-size-complex="12pt" style:language-complex="hi" style:country-complex="IN" fo:hyphenate="false" fo:hyphenation-remain-char-count="2" fo:hyphenation-push-char-count="2"/>
    </style:default-style>
    <style:default-style style:family="table">
      <style:table-properties table:border-model="collapsing"/>
    </style:default-style>
    <style:default-style style:family="table-row">
      <style:table-row-properties fo:keep-together="auto"/>
    </style:default-style>
    <style:style style:name="Standard" style:family="paragraph" style:class="text" style:master-page-name="">
      <style:paragraph-properties fo:line-height="150%" fo:text-align="justify" style:justify-single-word="false" style:page-number="auto">
        <style:tab-stops/>
      </style:paragraph-properties>
      <style:text-properties style:font-name="Times New Roman" fo:font-family="'Times New Roman'" style:font-style-name="Normal" style:font-family-generic="roman" style:font-pitch="variable" fo:font-size="14pt"/>
    </style:style>
    <style:style style:name="CodeBlock" style:family="paragraph" style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false" fo:text-align="start" style:justify-single-word="false" fo:keep-with-next="always"/>
      <style:text-properties style:font-name="FreeMono1" fo:font-family="FreeMono" style:font-style-name="Normal" style:font-family-generic="modern" style:font-pitch="fixed" fo:font-size="14pt"/>
    </style:style>
    <style:style style:name="PageBreak" style:family="paragraph" style:parent-style-name="Text_Body">
      <style:paragraph-properties fo:break-after="page"/>
    </style:style>
    <style:style style:name="Heading" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_Body" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false" fo:text-align="center" style:justify-single-word="false" fo:keep-with-next="always"/>
      <style:text-properties style:font-name="Times New Roman" fo:font-family="'Times New Roman'" style:font-style-name="Normal" style:font-family-generic="roman" style:font-pitch="variable" fo:font-size="14pt" style:font-name-asian="DejaVu Sans" style:font-family-asian="'DejaVu Sans'" style:font-family-generic-asian="system" style:font-pitch-asian="variable" style:font-size-asian="14pt" style:font-name-complex="FreeSans1" style:font-family-complex="FreeSans" style:font-family-generic-complex="system" style:font-pitch-complex="variable" style:font-size-complex="14pt"/>
    </style:style>
    <style:style style:name="Text_Body" style:display-name="Text body" style:family="paragraph" style:parent-style-name="Standard" style:class="text">
      <style:paragraph-properties fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false" fo:text-indent="1.251cm" style:auto-text-indent="false"/>
    </style:style>
    <style:style style:name="List" style:family="paragraph" style:parent-style-name="Text_Body" style:class="list">
      <style:text-properties style:font-size-asian="12pt" style:font-name-complex="FreeSans" style:font-family-complex="FreeSans" style:font-style-name-complex="Normal" style:font-family-generic-complex="swiss" style:font-pitch-complex="variable"/>
    </style:style>
    <style:style style:name="Caption" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false" text:number-lines="false" text:line-number="0"/>
      <style:text-properties fo:font-size="14pt" fo:font-style="normal" style:font-size-asian="12pt" style:font-style-asian="italic" style:font-name-complex="Times New Roman" style:font-family-complex="'Times New Roman'" style:font-style-name-complex="Normal" style:font-family-generic-complex="roman" style:font-pitch-complex="variable" style:font-size-complex="12pt" style:font-style-complex="italic"/>
    </style:style>
    <style:style style:name="Index" style:family="paragraph" style:parent-style-name="Standard" style:class="index">
      <style:paragraph-properties text:number-lines="false" text:line-number="0"/>
      <style:text-properties style:font-size-asian="12pt" style:font-name-complex="FreeSans" style:font-family-complex="FreeSans" style:font-style-name-complex="Normal" style:font-family-generic-complex="swiss" style:font-pitch-complex="variable"/>
    </style:style>
    <style:style style:name="Title" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:class="chapter">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="28pt" style:font-weight-asian="bold" style:font-size-complex="28pt" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_1" style:display-name="Heading 1" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="1" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="130%" style:font-weight-asian="bold" style:font-size-complex="130%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_2" style:display-name="Heading 2" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="2" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="115%" style:font-weight-asian="bold" style:font-size-complex="115%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_3" style:display-name="Heading 3" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="3" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="101%" style:font-weight-asian="bold" style:font-size-complex="101%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_4" style:display-name="Heading 4" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="4" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-style="normal" fo:font-weight="bold" style:font-size-asian="95%" style:font-style-asian="italic" style:font-weight-asian="bold" style:font-size-complex="95%" style:font-style-complex="italic" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_5" style:display-name="Heading 5" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="5" style:class="text">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="10.5pt" style:font-weight-asian="bold" style:font-size-complex="12pt" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Index_Heading" style:display-name="Index Heading" style:family="paragraph" style:parent-style-name="Heading" style:class="index">
      <style:paragraph-properties fo:margin-left="0cm" fo:margin-right="0cm" fo:text-indent="0cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="16pt" style:font-weight-asian="bold" style:font-size-complex="16pt" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Appendix" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="1" style:list-style-name="" style:class="chapter">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="16pt" style:font-weight-asian="bold" style:font-size-complex="16pt" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Footnote" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
      <style:paragraph-properties fo:margin-left="0.598cm" fo:margin-right="0cm" fo:text-indent="-0.598cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
      <style:text-properties fo:font-size="14pt" style:font-size-asian="10pt" style:font-size-complex="10pt"/>
    </style:style>
    <style:style style:name="Endnote" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
      <style:paragraph-properties fo:margin-left="0.598cm" fo:margin-right="0cm" fo:text-indent="-0.598cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
      <style:text-properties fo:font-size="14pt" style:font-size-asian="10pt" style:font-size-complex="10pt"/>
    </style:style>
    <style:style style:name="Preformatted_Text" style:display-name="Preformatted Text" style:family="paragraph" style:parent-style-name="Standard" style:class="html">
      <style:paragraph-properties fo:margin-top="0cm" fo:margin-bottom="0cm" style:contextual-spacing="false"/>
      <style:text-properties style:font-name="FreeMono" fo:font-family="FreeMono" style:font-family-generic="modern" style:font-pitch="fixed" fo:font-size="12pt" style:font-name-asian="FreeMono" style:font-family-asian="FreeMono" style:font-family-generic-asian="modern" style:font-pitch-asian="fixed" style:font-size-asian="10pt" style:font-name-complex="FreeMono" style:font-family-complex="FreeMono" style:font-family-generic-complex="modern" style:font-pitch-complex="fixed" style:font-size-complex="10pt"/>
    </style:style>
    <style:style style:name="Heading_6" style:display-name="Heading 6" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="6" style:class="text">
      <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.106cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-style="normal" fo:font-weight="bold" style:font-size-asian="10.5pt" style:font-style-asian="italic" style:font-weight-asian="bold" style:font-size-complex="12pt" style:font-style-complex="italic" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Drawing" style:family="paragraph" style:parent-style-name="Caption" style:class="extra">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
    </style:style>
    <style:style style:name="Table" style:family="paragraph" style:parent-style-name="Caption" style:class="extra">
      <style:paragraph-properties fo:text-align="start" style:justify-single-word="false"/>
    </style:style>
    <style:style style:name="Illustration" style:family="paragraph" style:parent-style-name="Caption" style:class="extra">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
    </style:style>
    <style:style style:name="Figure" style:family="paragraph" style:parent-style-name="Caption" style:class="extra">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false"/>
    </style:style>
    <style:style style:name="Header_and_Footer" style:display-name="Header and Footer" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">
      <style:paragraph-properties fo:text-align="center" style:justify-single-word="false" text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Header" style:family="paragraph" style:parent-style-name="Header_and_Footer" style:class="extra">
      <style:paragraph-properties text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Header_left" style:display-name="Header left" style:family="paragraph" style:parent-style-name="Header" style:class="extra">
      <style:paragraph-properties fo:text-align="start" style:justify-single-word="false" text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Header_right" style:display-name="Header right" style:family="paragraph" style:parent-style-name="Header" style:class="extra">
      <style:paragraph-properties fo:text-align="end" style:justify-single-word="false" text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Footer" style:family="paragraph" style:parent-style-name="Header_and_Footer" style:class="extra">
      <style:paragraph-properties text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Footer_left" style:display-name="Footer left" style:family="paragraph" style:parent-style-name="Footer" style:class="extra">
      <style:paragraph-properties fo:text-align="start" style:justify-single-word="false" text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Footer_right" style:display-name="Footer right" style:family="paragraph" style:parent-style-name="Footer" style:class="extra">
      <style:paragraph-properties fo:text-align="end" style:justify-single-word="false" text:number-lines="false" text:line-number="0">
        <style:tab-stops>
          <style:tab-stop style:position="8.5cm" style:type="center"/>
          <style:tab-stop style:position="17cm" style:type="right"/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Contents_Heading" style:display-name="Contents Heading" style:family="paragraph" style:parent-style-name="Index_Heading" style:class="index">
      <style:paragraph-properties fo:margin-left="0cm" fo:margin-right="0cm" fo:text-indent="0cm" style:auto-text-indent="false" text:number-lines="false" text:line-number="0"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="16pt" style:font-weight-asian="bold" style:font-size-complex="16pt" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Contents_1" style:display-name="Contents 1" style:family="paragraph" style:parent-style-name="Index" style:class="index">
      <style:paragraph-properties fo:margin-left="0cm" fo:margin-right="0cm" fo:text-indent="0cm" style:auto-text-indent="false">
        <style:tab-stops>
          <style:tab-stop style:position="16.501cm" style:type="right" style:leader-style="dotted" style:leader-text="."/>
        </style:tab-stops>
      </style:paragraph-properties>
    </style:style>
    <style:style style:name="Subtitle" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:class="chapter">
      <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.212cm" style:contextual-spacing="false" fo:text-align="center" style:justify-single-word="false"/>
      <style:text-properties fo:font-size="14pt" style:font-size-asian="18pt" style:font-size-complex="18pt"/>
    </style:style>
    <style:style style:name="Heading_7" style:display-name="Heading 7" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="7" style:class="text">
      <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.106cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="80%" style:font-weight-asian="bold" style:font-size-complex="80%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_8" style:display-name="Heading 8" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="8" style:class="text">
      <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.106cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-style="normal" fo:font-weight="bold" style:font-size-asian="80%" style:font-style-asian="italic" style:font-weight-asian="bold" style:font-size-complex="80%" style:font-style-complex="italic" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_9" style:display-name="Heading 9" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="9" style:class="text">
      <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.106cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="75%" style:font-weight-asian="bold" style:font-size-complex="75%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Heading_10" style:display-name="Heading 10" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_Body" style:default-outline-level="10" style:class="text">
      <style:paragraph-properties fo:margin-top="0.106cm" fo:margin-bottom="0.106cm" style:contextual-spacing="false"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold" style:font-size-asian="75%" style:font-weight-asian="bold" style:font-size-complex="75%" style:font-weight-complex="bold"/>
    </style:style>
    <style:style style:name="Quotations" style:family="paragraph" style:parent-style-name="Standard" style:class="html">
      <style:paragraph-properties fo:margin-left="1cm" fo:margin-right="1cm" fo:margin-top="0cm" fo:margin-bottom="0.499cm" style:contextual-spacing="false" fo:text-indent="0cm" style:auto-text-indent="false"/>
    </style:style>
    <style:style style:name="Bullet_Symbols" style:display-name="Bullet Symbols" style:family="text">
      <style:text-properties style:font-name="Times New Roman" fo:font-family="'Times New Roman'" style:font-style-name="Normal" style:font-family-generic="roman" style:font-pitch="variable" style:font-charset="x-symbol" style:font-name-asian="Times New Roman" style:font-family-asian="'Times New Roman'" style:font-style-name-asian="Normal" style:font-family-generic-asian="roman" style:font-pitch-asian="variable" style:font-name-complex="Times New Roman" style:font-family-complex="'Times New Roman'" style:font-style-name-complex="Normal" style:font-family-generic-complex="roman" style:font-pitch-complex="variable"/>
    </style:style>
    <style:style style:name="Numbering_Symbols" style:display-name="Numbering Symbols" style:family="text"/>
    <style:style style:name="Internet_link" style:display-name="Internet link" style:family="text">
      <style:text-properties fo:color="#000080" fo:language="zxx" fo:country="none" style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="font-color" style:language-asian="zxx" style:country-asian="none" style:language-complex="zxx" style:country-complex="none"/>
    </style:style>
    <style:style style:name="Index_Link" style:display-name="Index Link" style:family="text"/>
    <style:style style:name="Graphics" style:family="graphic">
      <style:graphic-properties text:anchor-type="paragraph" svg:x="0cm" svg:y="0cm" style:wrap="none" style:vertical-pos="top" style:vertical-rel="paragraph" style:horizontal-pos="center" style:horizontal-rel="paragraph"/>
    </style:style>
    <style:style style:name="Frame" style:family="graphic">
      <style:graphic-properties text:anchor-type="paragraph" svg:x="0cm" svg:y="0cm" fo:margin-left="0.201cm" fo:margin-right="0.201cm" fo:margin-top="0.201cm" fo:margin-bottom="0.201cm" style:wrap="none" style:vertical-pos="top" style:vertical-rel="paragraph-content" style:horizontal-pos="center" style:horizontal-rel="paragraph-content" fo:padding="0.15cm" fo:border="0.06pt solid #000000"/>
    </style:style>
    <text:outline-style style:name="Outline">
      <text:outline-level-style text:level="1" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="2" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="3" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="4" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="5" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="6" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="7" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="8" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="9" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
      <text:outline-level-style text:level="10" style:num-format="">
        <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">
          <style:list-level-label-alignment text:label-followed-by="listtab"/>
        </style:list-level-properties>
      </text:outline-level-style>
    </text:outline-style>
    <text:notes-configuration text:note-class="footnote" style:num-format="1" text:start-value="0" text:footnotes-position="page" text:start-numbering-at="document"/>
    <text:notes-configuration text:note-class="endnote" style:num-format="i" text:start-value="0"/>
    <text:linenumbering-configuration text:number-lines="false" text:offset="0.499cm" style:num-format="1" text:number-position="left" text:increment="5"/>
  </office:styles>
  <office:automatic-styles>
    <style:page-layout style:name="Mpm1">
      <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="3cm" fo:margin-right="1.499cm" style:writing-mode="lr-tb" style:layout-grid-color="#c0c0c0" style:layout-grid-lines="20" style:layout-grid-base-height="0.706cm" style:layout-grid-ruby-height="0.353cm" style:layout-grid-mode="none" style:layout-grid-ruby-below="false" style:layout-grid-print="false" style:layout-grid-display="false" style:footnote-max-height="0cm">
        <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:line-style="solid" style:adjustment="left" style:rel-width="25%" style:color="#000000"/>
      </style:page-layout-properties>
      <style:header-style/>
      <style:footer-style/>
    </style:page-layout>
  </office:automatic-styles>
  <office:master-styles>
    <style:master-page style:name="Standard" style:page-layout-name="Mpm1"/>
  </office:master-styles>
</office:document-styles>
'''

meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ooo="http://openoffice.org/2004/office" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" office:version="1.3">
<office:meta>
  <meta:generator>MatomeruMI</meta:generator>
  <dc:title></dc:title>
  <meta:initial-creator>MatomeruMI</meta:initial-creator>
  <meta:editing-cycles>1</meta:editing-cycles>
  <dc:date>{datetimestring}</dc:date>
  <meta:creation-date>{datetimestring}</meta:creation-date>
  <dc:creator>MMI</dc:creator>
 </office:meta>
</office:document-meta>
'''

manifest_rdf = '''<?xml version="1.0" encoding="utf-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about="styles.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#StylesFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <ns0:hasPart xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" rdf:resource="styles.xml"/>
  </rdf:Description>
  <rdf:Description rdf:about="content.xml">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/odf#ContentFile"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <ns0:hasPart xmlns:ns0="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#" rdf:resource="content.xml"/>
  </rdf:Description>
  <rdf:Description rdf:about="">
    <rdf:type rdf:resource="http://docs.oasis-open.org/ns/office/1.2/meta/pkg#Document"/>
  </rdf:Description>
</rdf:RDF>
'''

manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3" xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0">
    <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text"/>{string}
</manifest:manifest>
'''
manifest_item = '\n <manifest:file-entry manifest:full-path="{name}" manifest:media-type="{mediatype}"/>'
