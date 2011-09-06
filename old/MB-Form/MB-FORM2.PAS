Uses Crt,Dos,Drivers;
{$I Zahl.Prc}
{$I Datei.Prc}
Var
d1,d2,d3:Text;
Attr1,Attr2:Word;
AktlForm,i,j,k:Integer;
Gr,AktlGr:LongInt;
Ch:Char;
Dat:Array[1..3]of String;
s1,s2,s3:String;

Function Ja:Boolean;Var Ch:Char;
Begin Ch:=ReadKey;While (UpCase(Ch)<>'J')And(UpCase(Ch)<>'N')
do Ch:=ReadKey;Ja:=UpCase(Ch)='J';End;

Procedure Meldung(s1,s2:String);
Begin
TextColor(LightCyan);GotoXY(1,4);Write(s1);ClrEol;
GotoXY(1,5);Write(s2);ClrEol;TextColor(Black);
GotoXY(79,1);Write('€');TextColor(Yellow);GotoXY(79,1);
End;

Begin
TextMode(Co80);TextColor(LightGreen);TextBackground(Black);ClrScr;
WriteLn('MB  Chronikumformer  Version II');
WriteLn('Von Matthias Bock - 1999');
WriteLn;TextColor(LightMagenta);
Write('Name der AHN-datei: ');ReadLn(Dat[1]);
Write('Name der TXT-datei: ');ReadLn(Dat[3]);
Dat[2]:='Format.ahn';
if DExis(Dat[1])And DExis(Dat[2])
then begin
     Meldung('ôffne angegebene Dateien ...','');
     AktlGr:=1;Gr:=DGr(Dat[1]);
     Assign(d1,Dat[1]);GetFAttr(d1,Attr1);SetFAttr(d1,Archive);Reset(d1);
     Assign(d2,Dat[2]);GetFAttr(d2,Attr2);SetFAttr(d2,Archive);Reset(d2);
     Assign(d3,Dat[3]);
     if DExis(Dat[3])
     then begin
          Meldung('Die Datei '+Dat[3]+' existiert bereits .',
          'Soll sie wirklich Åberschrieben werden (J/N) ?');
          if (Ja)then begin SetFAttr(d3,Archive);Erase(d3);end
          else begin
               Meldung('Programm aufgrung unzureichenden',
               'Inputs beendet .');Halt(1);
               end;
          end;ReWrite(d3);
     Meldung('ôffnungsvorgang fehlerfrei abgeschlossen !',
     'Analysiere Formatdatei '+Dat[2]+' ...');s1:='';
     While not eof (d2)
     do begin
        Read(d2,Ch);Ch:=UpCase(Ch);
        if ((Ord(Ch)>47)And(Ord(Ch)<58))
        Or (Ch='B')Or (Ch='Z')then s1:=s1+Ch;
        end;
     Close(d2);SetFAttr(d2,Attr2);AktlForm:=1;k:=0;
     Meldung('Analyse komplett !','Beginne Umschreibung von '+Dat[1]+' .');
     While (AktlGr<Gr)
     do begin
        Ch:=UpCase(s1[AktlForm]);AktlForm:=AktlForm+1;s2:='';s3:='';
        While (AktlForm<=Length(s1))And(Ord(s1[AktlForm])<58)
        do begin s2:=s2+s1[AktlForm];AktlForm:=AktlForm+1;end;
        if (Ch='Z')
        then begin
             Read(d1,Ch);AktlGr:=AktlGr+1;Str(Ord(Ch),s3);
             for i:=1 to StrZahl(s2)-1 do
             begin Read(d1,Ch);AktlGr:=AktlGr+1;end;
             if (Length(s3)=1)And((s3[1]='0')Or(s3[1]=' '))then s3:='';
             end else
        if (Ch='B')
        then begin
             for i:=1 to StrZahl(s2)
             do begin Read(d1,Ch);s3:=s3+Ch;AktlGr:=AktlGr+1;end;
             end;
        i:=Length(s3);
        While (s3[i]=' ')And(i>1)
        do begin
           s2:=s3;s3:='';i:=i-1;
           for j:=1 to Length(s2)-1 do s3:=s3+s2[j];
           end;
        for i:=1 to Length(s3)
        do begin
           if (Ord(s3[i])=228)then s3[i]:='Ñ';
           if (Ord(s3[i])=246)then s3[i]:='î';
           if (Ord(s3[i])=252)then s3[i]:='Å';
           end;
        if (Length(s3)=1)And((Ord(s3[1])<49)Or(Ord(s3[1])>160))then s3:='';
        Write(d3,s3+';');
        if (AktlForm>=Length(s1))
        then begin
             AktlForm:=1;WriteLn(d3,'');k:=k+1;
             Str(k,s2);Meldung('Familienangehîrige :',s2);
             end;
        if KeyPressed then begin Close(d1);Close(d3);end;
        end;
     Close(d1);SetFAttr(d1,Attr1);Close(d3);SetFAttr(d3,Archive);
     Meldung('Umschreibung abgeschlossen !',
     'Gefundene Daten in '+Dat[3]+' gesichert .');
     TextColor(LightMagenta);TextBackground(Black);GotoXY(1,7);
     end
else Meldung('Datei nicht gefunden .','Programm nicht ausfÅhrbar !');
Ch:=ReadKey;
End.