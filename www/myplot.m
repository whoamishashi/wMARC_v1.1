 
  % myplot.m

  plot( randn(100,1) )

  % get local time

  lt=localtime(time())
  hr_min= lt.hour+(lt.min)/60;
  hr_sec= lt.hour+(lt.sec)/60;
 
  title_text1 = num2str(hr_min);
  title_text2 = num2str(hr_sec);
  
  title_text3= strcat(round(title_text1),"-"); 

  title(strcat(title_text3,round(title_text2)))
  
  print("myplot.png","-dpng")

