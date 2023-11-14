$(function() {//控制preview文件内容生成
			var surveyHtml = localStorage.getItem('surveyHtml');
			$("#survey-wrap").html(surveyHtml);
			$(".sur-container").css("margin", "10px auto");
			$(".edit-area").attr("contenteditable", true).removeClass("edit-area");
			//编辑css样式3
			$(".add-area, .operate").hide();
			$('.describe').css({"background-color": "#f1f5fd", "border-color": "#f1f5fd"});
			$(".survey-title").css({"font-size": '28px', "color": '#333', "margin": '20px 0', "border": "none"})
			$(".ques-block").css({"background-color": "#eee"});
			$(".topic-type-question").css({"border": "none"});
			
			$("#survey-wrap").append("<div id='submitbtn' class = 'submit-survey'>SUbmit</div>")
			$("#submitbtn").click(function(){
				localStorage.setItem('QuestionAnswer','blank');
				localStorage.setItem('QuestionCount',parseInt(localStorage.getItem('NumofSurveryQuestion')));
				for(i=0;i<parseInt(localStorage.getItem('NumofSurveryQuestion'));i++){
				AnswerList[i] = i;
				}
				localStorage.setItem('AnswerList',AnswerList);	
				getIds();
				getNames();
				//console.log("所获取的选择题id集合-ChoiceIdList："+ChoiceIdList);
				//console.log("所获取的填空题id集合-BlankIdList："+BlankIdList);
				console.log("所获取的name集合-ChoiceNameList:"+ChoiceNameList);
				getChoiceText();
				console.log("选择的选项-SelectionList："+SelectionList);
				console.log("所有问题数据对象--不是答案，是题干！！见下方----QuestionBoxObject： ");
				console.log(QuestionBoxObject);
				splitChoices();
				getAnswers();
				for (i in AnswerBoxObject){
					wenjuan_ans.push(AnswerBoxObject[i]);
				}
				 $.post("/yuyue_survey_preview",{
					 wenjuan_ans : wenjuan_ans,
				});
					alert("提交问卷数据");				
				}) 
				
		})
var ChoiceIdList = new Array();
var ChoiceNameList = new Array();
var BlankIdList = new Array();
var SelectionList = new Array();
var wenjuan_ans = new Array();
function getIds(){//获取一个遍历所有问题id的object变量。用于获取其他内容
		$("input").each(function(index){
		ChoiceIdList.push($(this).attr("id"));
	})
		$("textarea").each(function(index){
		BlankIdList.push($(this).attr("id"));
	})
}
function getNames(){//获取一个遍历所有问题id的object变量。用于获取其他内容
		$("input").each(function(index){
		ChoiceNameList.push($(this).attr("name"));
	})
		$("textarea").each(function(index){
		ChoiceNameList.push($(this).attr("name"));
	})
}
function getChoiceText(){//根据问题数量返回所有问题的文本。Submit按钮后触发
		for(i=0;i<ChoiceIdList.length;i++){
			SelectionList[i] = $(".choice-text")[i].innerText;
		}
		
}
var QuestionBoxObject={
	"Question1":{id:1,type:"无",choiceText:[]}
};
var AnswerBoxObject ={
	"Answer":[]
}
function splitChoices(){//将所有问题从分离的html部分中提取至一个相同的object中，便于后面利用
	for(k=1;k<(AnswerList.length+1);k++){
		QuestionBoxObject["Question"+k] = {//初始化
		type:"填空题",
		choiceText:[],
		}
	}
	for(j=0;j<(ChoiceIdList.length-1);j++){
			if((ChoiceIdList[j].split("o"))[1][0].charCodeAt() != 120){
				if ((ChoiceIdList[j].split("o"))[1] == (ChoiceIdList[j+1].split("o"))[1]){//与下一个相同，应当添加的是问题文本
					var TempId = ChoiceIdList[j].split("o")[1];
					//console.log("TEMPID: "+TempId);
					QuestionBoxObject["Question"+TempId].type="单选题";
					QuestionBoxObject["Question"+TempId].choiceText.push(SelectionList[j]);
				}else{
					if ((ChoiceIdList[j].split("o"))[1] == (ChoiceIdList[j-1].split("o"))[1]){
						var TempId = ChoiceIdList[j].split("o")[1];
						QuestionBoxObject["Question"+TempId].type="单选题";
						QuestionBoxObject["Question"+TempId].choiceText.push(SelectionList[j]);
					}
				}
			}else{
				if ((ChoiceIdList[j].split("x"))[1] == (ChoiceIdList[j+1].split("x"))[1]){//与下一个相同，应当添加的是问题文本
					var TempId = ChoiceIdList[j].split("x")[1];
					//console.log("J"+j);
					QuestionBoxObject["Question"+TempId].type="多选题";
					QuestionBoxObject["Question"+TempId].choiceText.push(SelectionList[j]);
				}else{
					if ((ChoiceIdList[j].split("x"))[1] == (ChoiceIdList[j-1].split("x"))[1]){
						var TempId = ChoiceIdList[j].split("x")[1];
						//console.log(TempId);
						QuestionBoxObject["Question"+TempId].type="多选题";
						QuestionBoxObject["Question"+TempId].choiceText.push(SelectionList[j]);
					}
				}
			}
	}
	if((ChoiceIdList[j].split("o"))[1][0].charCodeAt() != 120){
		var TempId = ChoiceIdList[(ChoiceIdList.length-1)].split("o")[1];//加入脱离循环的最后一个选择项
		//console.log("特殊值-----------"+j)
		QuestionBoxObject["Question"+TempId].type="单选题";
		QuestionBoxObject["Question"+TempId].choiceText.push(SelectionList[TempId]);
	}else{
		var TempId = ChoiceIdList[(ChoiceIdList.length-1)].split("x")[1];//加入脱离循环的最后一个选择项
		//console.log("特殊值-----------"+j)
		QuestionBoxObject["Question"+TempId].type="多选题";
		QuestionBoxObject["Question"+TempId].choiceText.push(SelectionList[TempId]);
	}
}
function getAnswers(){
	var AnswerText =[];
	for(j=0;j<ChoiceNameList.length;j++){//j为索引，以所有选项个数为总和
		if((document.getElementsByName(ChoiceNameList[j])[0]).checked){
			if((document.getElementsByName(ChoiceNameList[j])[0]).type == "checkbox"){//创建一个数组保存
				var MutBox=[];
				MutBox.push($(".choice-text")[j].innerText);
				AnswerBoxObject.Answer.push(MutBox);
			}else{
				AnswerBoxObject.Answer.push($(".choice-text")[j].innerText);	
			}
		}else if((document.getElementsByName(ChoiceNameList[j])[0]).type == "textarea"){
			AnswerBoxObject.Answer.push(document.getElementsByName(ChoiceNameList[j])[0].value);	
		}
	}
	console.log("获得答案的object-见下：AnswerBoxObject ");
	console.log(AnswerBoxObject);
}

function search(arr,dst){
    var i = arr.length;
    for(j=0;j<i;i++){
        if (arr[j] == dst){
           return j;
        }
    }
    return false;
}