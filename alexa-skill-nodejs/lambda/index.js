// This skill connects to the EV3 MINDSTORMS Printer Bot Gadget.
//
// Jason Allemann
//
const Alexa = require( 'ask-sdk-core' );
const Util = require( './util' );
const Common = require( './common' );

// The custom directive to be sent by this skill
const NAMESPACE = 'Custom.Mindstorms.Gadget';
const NAME_CONTROL = 'control';

// The standard print prompt, used throughout the skill.
const PrintPrompt = "What would you like to print?"

const LaunchRequestHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle: async function(handlerInput)
    {
        let request = handlerInput.requestEnvelope;
        let { apiEndpoint, apiAccessToken } = request.context.System;
        let apiResponse = await Util.getConnectedEndpoints(apiEndpoint, apiAccessToken);
        if ((apiResponse.endpoints || []).length === 0)
        {
            return handlerInput.responseBuilder
            .speak(`I couldn't find an EV3 Brick connected to this Echo device.`)
            .getResponse();
        }

        // Store the gadget endpointId to be used in this skill session
        let endpointId = apiResponse.endpoints[0].endpointId || [];
        Util.putSessionAttribute(handlerInput, 'endpointId', endpointId);

        return handlerInput.responseBuilder
            .speak( PrintPrompt )
            .reprompt( PrintPrompt )
            .getResponse();
    }
};

//
// Handler to get the text size.
// Sends a directive to the EV3 brick to get the text size and starts the event handler
// to listen for the response.
//
const GetTextSizeIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'GetTextSizeIntent';
    },
    handle: function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log('--- GetTextSizeIntent handler. ---');

        // Build the directive to get the text size from the EV3.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'getTextSize' } );

        // Set the token to track the event handler
        const token = handlerInput.requestEnvelope.request.requestId;
        Util.putSessionAttribute( handlerInput, 'token', token );

        return handlerInput.responseBuilder
            .addDirective( directive )
            .addDirective( Util.buildStartEventHandler( token, 5000, {} ) )
            .getResponse();
    }
};

//
// Handler to set the text size, in millimeters.
// The text size will be stored on the EV3 to be remembered for future sessions.
//
const SetTextSizeIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'SetTextSizeIntent';
    },
    handle: function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log('--- SetTextSizeIntent handler. ---');

        let textSize = Alexa.getSlotValue( handlerInput.requestEnvelope, 'TextSize' );
        textSize = Math.max(3, Math.min(8, parseInt(textSize)));

        // Build the directive to set the text size on the EV3.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'setTextSize', size: textSize } );

        return handlerInput.responseBuilder
            .speak( `Setting the text size to ${textSize} millimeters.` )
            .reprompt( PrintPrompt )
            .addDirective(directive)
            .getResponse();
    }
};

//
// Handler for the setting the dialog mode on or off.
// The on/off slot is optional. If it doesn't exist, dialog mode will be turned on.
//
const SetDialogModeIntentHandler = {
    canHandle( handlerInput )
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'SetDialogModeIntent';
    },
    handle: function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log('--- SetDialogMode handler ---');

        let onOff = "on";
        if( handlerInput.requestEnvelope.request.intent.slots.DialogMode.value &&
            handlerInput.requestEnvelope.request.intent.slots.DialogMode.resolutions.resolutionsPerAuthority[0].status.code === "ER_SUCCESS_MATCH" )
        {
            onOff = handlerInput.requestEnvelope.request.intent.slots.DialogMode.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        }

        // Build the directive to set the dialog mode on the EV3.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'dialogMode', enable: onOff } );

        return handlerInput.responseBuilder
            .speak( `Turning dialog mode ${onOff}.` )
            .reprompt( PrintPrompt )
            .addDirective( directive )
            .getResponse();
    }
};


//
// Handler for the setting a spoken word.
// The word will be in the 'Word' slot.
//
const PrintWordIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'PrintWordIntent';
    },
    handle: function (handlerInput)
    {
        const request = handlerInput.requestEnvelope;
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];

        let word = Alexa.getSlotValue( handlerInput.requestEnvelope, 'Word' );

        // Build the directive to have the EV3 print the word.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'print', word: word } );

        return handlerInput.responseBuilder
            .speak( `printing ${word}` )
            .addDirective(directive)
            .getResponse();
    }
};

//
// Handler for the calibration intent.
// Activates the calibration mode of the printer.
// While in calibration mode, the user can adjust the height of the pen using the up and down buttons,
// and exit the calibration mode by pressing the enter button.
//
const CalibrateIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'CalibrateIntent';
    },
    handle: function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log( '#### Calibrate handler. ####' );

        if( handlerInput.requestEnvelope.request.intent.confirmationStatus === "DENIED" )
        {
            return handlerInput.responseBuilder
                .speak( PrintPrompt )
                .reprompt( PrintPrompt )
                .getResponse();
        }

        // Build the directive to activate the calibration mode.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'calibrate' } );

        return handlerInput.responseBuilder
            .speak( `Entering calibration mode.` )
            .addDirective( directive )
            .getResponse();
    }
};

//
// This function gets one of the default lists, based on the suffix of the list_id.
// The default To-Do and Shopping lists list_id values are base-64 encoded strings with these formats:
//  <Internal_identifier>-TASK for the to-do list
//  <Internal_identifier>-SHOPPING_ITEM for the shopping list
//
async function getDefaultList( handlerInput, suffix )
{
    const attributesManager = handlerInput.attributesManager;
    let listId;

    const listClient = handlerInput.serviceClientFactory.getListManagementServiceClient();
    const listOfLists = await listClient.getListsMetadata();
    if( !listOfLists )
    {
      console.log('Permissions are not defined.');
      return null;
    }

    for( let i = 0; i < listOfLists.lists.length; i += 1 )
    {
        const decodedListId = Buffer.from(listOfLists.lists[i].listId, 'base64' ).toString( 'utf8' );
        if( decodedListId.endsWith( suffix ) )
        {
            console.log( `Found ${listOfLists.lists[i].name} with id ${listOfLists.lists[i].listId}` );
            console.log( `Decoded listId: ${decodedListId}` );
            listId = listOfLists.lists[i].listId;
            break;
        }
    }

    return listId;
}

//
// This function gets  a list by it's name. These will all be custom created lists by the user.
//
async function getListByName( handlerInput, name )
{
    const attributesManager = handlerInput.attributesManager;

    const listClient = handlerInput.serviceClientFactory.getListManagementServiceClient();
    const listOfLists = await listClient.getListsMetadata();
    if( !listOfLists )
    {
      console.log('Permissions are not defined.');
      return null;
    }

    let listId;
    for( let i = 0; i < listOfLists.lists.length; i += 1 )
    {
        if( name.toLowerCase() === listOfLists.lists[i].name.toLowerCase() )
        {
            console.log( `Found ${listOfLists.lists[i].name} with id ${listOfLists.lists[i].listId}` );
//            console.log( `Matched ${listOfLists.lists[i].name} with listId: ${listOfLists.lists[i].listId}` );
            listId = listOfLists.lists[i].listId;
            break;
        }
    }

    return listId;
}

//
// This function will get the id of the list corresponding to the 'ListName' slot in the request.
//
async function getListNameSlotListId( handlerInput )
{
    var listId = null;

    let slotValue = Alexa.getSlotValue(handlerInput.requestEnvelope, 'ListName');
    console.log( `# ListName slot value: ${slotValue}` );

    var slotId = "Custom List";
    if( handlerInput.requestEnvelope.request.intent.slots.ListName.resolutions.resolutionsPerAuthority[0].status.code === "ER_SUCCESS_MATCH" )
    {
        slotId = handlerInput.requestEnvelope.request.intent.slots.ListName.resolutions.resolutionsPerAuthority[0].values[0].value.id;
    }
    console.log( `# ListName slot Id: ${slotId}`);

    if( slotId === "ShoppingID")
    {
        listId = await getDefaultList( handlerInput, '-SHOPPING_ITEM' );
    }
    else if( slotId === "TodoID")
    {
        listId = await getDefaultList( handlerInput, '-TASK' );
    }
    else
    {
        listId = await getListByName( handlerInput, slotValue );
    }
    
    return listId;
}

//
// This function will return a simple list of the items in the specified list.
//
async function getListItems( handlerInput, listId )
{
  const listClient = handlerInput.serviceClientFactory.getListManagementServiceClient();
  const list = await listClient.getList( listId, 'active' );
  if( !list )
  {
    console.log( 'null list' );
    return null;
  }

  return list.items;
}

//
// Handler for the printing the items in a list.
// This function will get the items in the requested list, and build a directive for the EV3 to print them.
//
const PrintListIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'PrintListIntent';
    },
    handle: async function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        const responseBuilder = handlerInput.responseBuilder;

        if( handlerInput.requestEnvelope.request.intent.confirmationStatus === "DENIED" )
        {
            return handlerInput.responseBuilder
                .speak( PrintPrompt )
                .reprompt( PrintPrompt )
                .getResponse();
        }

        console.log( '#### Starting the print list handler. ####' );

        let listName = Alexa.getSlotValue(handlerInput.requestEnvelope, 'ListName');
        var listId = await getListNameSlotListId( handlerInput );

        console.log( `# Printing the items in the ${listName} list.` );

        var items = null;
        if( !listId )
        {
            return responseBuilder
                .speak( `I could not find a list named ${listName}.` )
                .reprompt( PrintPrompt )
                .getResponse();
        }
        else
        {
            items = await getListItems( handlerInput, listId );
        }

        if( !items )
        {
          const permissions = ['read::alexa:household:list'];
          return handlerInput.responseBuilder
            .speak( 'Alexa List permissions are missing.' )
            .withAskForPermissionsConsentCard( permissions )
            .getResponse();
        }
        else if( items.length === 0 )
        {
          return responseBuilder
            .speak( `The ${listName} list is empty.` )
            .reprompt( PrintPrompt )
            .getResponse();
        }

        var listItems = [];
        for( let i = 0; i < items.length; i += 1 )
        {
            const itemValue = items[i].value;
            listItems.push( itemValue );
        }

        // Build the directive for the EV3 to print the list items.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'printList', items: JSON.stringify(listItems) } );

        console.log( directive );
    
        return handlerInput.responseBuilder
            .speak( `Printing the list items.` )
            .addDirective( directive )
            .getResponse();
  }, 
}

//
// Handler for printing gift tags.
// This function will get the items (in this case names) in the requested list
// and build a directive for the EV3 to print gift tags for each one.
//
const GiftTagsIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'PrintGiftTagsIntent';
    },
    handle: async function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        const responseBuilder = handlerInput.responseBuilder;

        if( handlerInput.requestEnvelope.request.intent.confirmationStatus === "DENIED" )
        {
            return handlerInput.responseBuilder
                .speak( PrintPrompt )
                .reprompt( PrintPrompt )
                .getResponse();
        }

        console.log( '#### Starting the print gift tags handler. ####' );

        let sender = Alexa.getSlotValue(handlerInput.requestEnvelope, 'Sender');
        let listName = Alexa.getSlotValue(handlerInput.requestEnvelope, 'ListName');
        var listId = await getListNameSlotListId( handlerInput );

        console.log( `# Printing gift tags from ${sender} to the ${listName} list.` );

        var items = null;
        if( !listId )
        {
            return responseBuilder
                .speak( `I could not find a list named ${listName}.` )
                .reprompt( PrintPrompt )
                .getResponse();
        }
        else
        {
            items = await getListItems( handlerInput, listId );
        }

        if( !items )
        {
            const permissions = ['read::alexa:household:list'];
            return handlerInput.responseBuilder
                .speak( 'Alexa list permissions are missing.' )
                .withAskForPermissionsConsentCard(permissions)
                .getResponse();
        }
        else if( items.length === 0 )
        {
            return responseBuilder
                .speak( `The ${listName} list is empty.` )
                .reprompt( PrintPrompt )
                .getResponse();
        }

        var listItems = [];
        for( let i = 0; i < items.length; i += 1 )
        {
            listItems.push( items[i].value );
        }

        // Build the directive for the EV3 to print the gift tags.
        const directive = Util.build( endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'giftTags', items: JSON.stringify(listItems), sender: sender } );

        console.log( directive );

        return handlerInput.responseBuilder
            .speak( `Printing gift tags.` )
            .addDirective( directive )
            .getResponse();
    }, 
}

//
// Handler for printing the Mindstorms EV3 Logo
//
const MindstormsLogoIntentHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'IntentRequest'
            && Alexa.getIntentName(handlerInput.requestEnvelope) === 'MindstormsLogoIntent';
    },
    handle: function (handlerInput)
    {
        const attributesManager = handlerInput.attributesManager;
        const endpointId = attributesManager.getSessionAttributes().endpointId || [];
        console.log('#### Mindstorms logo handler. ####');

        if( handlerInput.requestEnvelope.request.intent.confirmationStatus === "DENIED" )
        {
            return handlerInput.responseBuilder
                .speak( PrintPrompt )
                .reprompt( PrintPrompt )
                .getResponse();
        }

        // Build the directive to print the mindstorms logo.
        const directive = Util.build(endpointId, NAMESPACE, NAME_CONTROL,
            { type: 'mindstorms' } );

        return handlerInput.responseBuilder
            .speak( `Printing the Mindstorms logo.` )
            .addDirective( directive )
            .getResponse();
    }
};

const EventsReceivedRequestHandler = {
    canHandle(handlerInput)
    {
        let { request } = handlerInput.requestEnvelope;
        console.log('Request type: ' + Alexa.getRequestType(handlerInput.requestEnvelope));
        if (request.type !== 'CustomInterfaceController.EventsReceived') return false;

        const attributesManager = handlerInput.attributesManager;
        let sessionAttributes = attributesManager.getSessionAttributes();
        let customEvent = request.events[0];

        // Validate event token
        if (sessionAttributes.token !== request.token)
        {
            console.log("Event token doesn't match. Ignoring this event");
            return false;
        }

        // Validate endpoint
        let requestEndpoint = customEvent.endpoint.endpointId;
        if (requestEndpoint !== sessionAttributes.endpointId)
        {
            console.log("Event endpoint id doesn't match. Ignoring this event");
            return false;
        }
        return true;
    },
    handle(handlerInput)
    {
        console.log("== Received Custom Event ==");
        let customEvent = handlerInput.requestEnvelope.request.events[0];
        let payload = customEvent.payload;
        let name = customEvent.header.name;

        let speechOutput;
        if (name === 'TextSize')
        {
            console.log("Received Text Size Commmand.");
            let textSize = parseInt(payload.size);
            speechOutput = `The text size is ${textSize} millimeters.`;
        }
        else
        {
            speechOutput = "Event not recognized.";
        }
        return handlerInput.responseBuilder
            .speak( speechOutput, "REPLACE_ALL" )
            .withShouldEndSession(false)
            .addDirective(Util.buildStopEventHandlerDirective( handlerInput ))
            .reprompt("What would you like me to print?")
            .getResponse();
    }
};

const ExpiredRequestHandler = {
    canHandle(handlerInput)
    {
        return Alexa.getRequestType(handlerInput.requestEnvelope) === 'CustomInterfaceController.Expired'
    },
    handle(handlerInput)
    {
        console.log( "== Custom Event Expiration Input ==" );

        // End skill session
        return handlerInput.responseBuilder
            .speak("Skill duration expired. Goodbye.")
            .withShouldEndSession(true)
            .getResponse();
    }
};

//
// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
//
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        SetTextSizeIntentHandler,
        GetTextSizeIntentHandler,
        SetDialogModeIntentHandler,
        PrintListIntentHandler,
        GiftTagsIntentHandler,
        MindstormsLogoIntentHandler,
        CalibrateIntentHandler,
        PrintWordIntentHandler,
        EventsReceivedRequestHandler,
        ExpiredRequestHandler,
        Common.HelpIntentHandler,
        Common.CancelAndStopIntentHandler,
        Common.SessionEndedRequestHandler,
        Common.IntentReflectorHandler, // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    )
    .addRequestInterceptors(Common.RequestInterceptor)
    .addErrorHandlers(
        Common.ErrorHandler,
    )
    .withApiClient( new Alexa.DefaultApiClient() )
    .lambda();
    
