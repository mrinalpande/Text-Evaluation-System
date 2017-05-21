#include<stdio.h>
#include<string.h>
#include<ctype.h>

float score_total, score_part, semi_score, max_score, min_score, total_score;

char l1[10]={'q','w','e','r','t','y','u','i','o','p'},
     l2[9]={'a','s','d','f','g','h','j','k','l'},
     l3[7]={'z','x','c','v','b','n','m'};

//Function to check character
int findchar(char fc,char cc){

int i;
printf("char to find = %c\n correct char =%c\n",fc,cc);

   for(i=0;i<10;i++){
        if(fc==l1[i]){
            printf("findchar line1\n");
                if(cc==l1[i-1]||cc==l1[i+1]){
                    return 1;
            }
        }

        else if(fc==l2[i]){
            printf("findchar line2\n");
                if(cc==l2[i-1]||cc==l2[i+1]){
                    return 1;
                }
        }

        else if(fc==l3[i]){
            printf("findchar line3\n");
                if(cc==l3[i-1]||cc==l3[i+1]){
                    return 1;
                }
        }
   }
   return 0;
}

//Function to calculate score on the basis of no of characters
int calculate_score(int nc){
    printf("no of char=%d\n",nc);
	max_score=1;
	total_score=min_score=0;
	score_part = 1/(float)nc;
	semi_score = 1/(float)(nc + ( 1 / (float)( nc ) ) );

    //printf("total_score = %f \n score_part= %f \n semi_score=%f\n",total_score,score_part,semi_score);

return 0;
}


//Function to check character function
char check(char w[]){
int i,no_of_char,max;
char correct_w[10]="smart";

    no_of_char= strlen(correct_w);

	calculate_score(no_of_char);

        for(i=0;i<no_of_char;i++){

            if(w[i]==correct_w[i+1]&&w[i+1]==correct_w[i]){
                total_score = total_score + semi_score;
            }

            else if( w[i] == correct_w[i]){
                    printf("correct\n");
                total_score= total_score + score_part;
            }
            else if(findchar(w[i],correct_w[i])){
                printf("left or right\n");
                total_score = total_score + semi_score;
            }
            else{
                printf("incorrect\n");
		        total_score= total_score + 0;
            }

        }

        if(total_score > 0.5){
                printf("Total Score = %f\n",total_score*100);
                printf("\nCorrect word: %s\nEntered word: %s",correct_w,w);

        }
        else{
            printf("Total Score = %f\n", total_score*100);
        }

}


int main(){
char word[48];
printf("Enter the word:");
gets(word);
check(word);
return 0;
}
