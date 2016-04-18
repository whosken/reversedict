ReverseDict = {
    lookup:function(description, callback, handleParsingFailed){
        ReverseDict.jsonpCallback = function(data){
            if(!data.suggestions){
                console.log('Error parsing response', data);
                if(handleParsingFailed)
                    return handleParsingFailed(data);
            }
            var parsedData = $.map(data.suggestions, ReverseDict.cleanData);
            callback(parsedData);
        };
        
        $.ajax({
            url:'https://reversedict.herokuapp.com/lookup/'+description,
            dataType:'jsonp',
            contentType:'application/json',
            jsonpCallback:'ReverseDict.jsonpCallback'
        });
    },
    
    cleanData:function(data){
        return {
            term:ReverseDict.cleanTerm(data.term),
            definitions:data.definitions,
            synonyms:$.map(data.synonyms, ReverseDict.cleanTerm),
        };
    },
    
    cleanTerm:function(term){
        return term.replace(/_/g,' ');
    },
};