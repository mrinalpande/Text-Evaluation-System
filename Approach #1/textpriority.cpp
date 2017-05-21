#include<iostream>
#include<string.h>
using namespace std;

int partialcheck(char r, char s)
{
  const char *l[3] = {"qwertyuiop","asdfghjkl","zxcvbnm"};
  for(int i=0;i<3;i++)
  {
    int n=strlen(l[i]);
    for(int j=0;j<n;j++)
    {
      if( r==l[i][j] )
      {
          if(s==l[i][j+1] || s==l[i][j-1])
            {
                return 1;
            }

      }
    }
  }
  return 0;
}

int main()
{
  char str[10]="smart", inp[10]="smsrt";
  int n=strlen(str), maxtrans, flag=0;
  maxtrans=n/4;
  double score=1.00, per_l;
  per_l=(double)1/n;
  for(int i=0;i<n;i++)
  {
    if(score < 0.5) { score=0;break; }
    if(str[i]!=inp[i])
    {

      if(inp[i+1]==str[i] && inp[i]==str[i+1])
      {
        if(flag==maxtrans)
        {
          score=0; break;
        }
        i++;
        score-=0.25*2*per_l;
        flag++;
      }
      else
        {
            if( partialcheck(str[i],inp[i]) ) score-=0.5*per_l;
            else
                score-= per_l;
        }
    }
  }
  cout<<"Final score for the word is: "<<score*100;
}
